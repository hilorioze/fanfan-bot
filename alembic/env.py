import asyncio
from logging.config import fileConfig

import alembic_postgresql_enum  # noqa: F401
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.replaceable_entity import register_entities
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from alembic.script import ScriptDirectory
from src.config import conf
from src.db.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
config.set_main_option(
    'sqlalchemy.url',
    conf.db.build_connection_str()
)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, process_revision_directives=process_revision_directives,)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


def process_revision_directives(context, revision, directives):
    # extract Migration
    migration_script = directives[0]
    # extract current head revision
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()

    if head_revision is None:
        # edge case with first migration
        new_rev_id = 1
    else:
        # default branch with incrementation
        last_rev_id = int(head_revision)
        new_rev_id = last_rev_id + 1
    # fill zeros up to 3 digits: 1 -> 001
    migration_script.rev_id = '{0:03}'.format(new_rev_id)


real_position_function = PGFunction(
    schema="public",
    signature="update_real_position()",
    definition="""
         RETURNS trigger
     LANGUAGE plpgsql
    AS $function$
        begin
            with sq as (
                select
                    id,
                    case when schedule.skip = false then
                        row_number() over (partition by schedule.skip order by schedule.position)
                    else
                        null
                    end as rn
                from schedule
            )
            update schedule
            set real_position = sq.rn
            from sq
            where schedule.id = sq.id;
            return null;
        END;
    $function$
    ;
    """
)

real_position_trigger = PGTrigger(
    schema="public",
    signature="update_real_position_trigger",
    on_entity="public.schedule",
    definition="""
        after insert or delete or update of skip, "position" 
        on public.schedule for each statement execute function update_real_position()
    """
)

register_entities([real_position_function, real_position_trigger])


if context.is_offline_mode():
    #asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run_migrations_offline()
else:
    #asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run_migrations_online()
