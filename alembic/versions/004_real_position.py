"""real_position

Revision ID: 004
Revises: 003
Create Date: 2023-09-02 13:50:20.845487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

# fmt: off
create_function = """CREATE OR REPLACE FUNCTION public.update_real_position()
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
;;
"""  # noqa

drop_function = "DROP FUNCTION public.update_real_position();"

create_trigger = """create trigger update_real_position_trigger 
after insert or delete or update of skip, "position" 
on public.schedule for each statement execute function update_real_position()"""

drop_trigger = """DROP TRIGGER update_real_position_trigger ON public.schedule;"""

# fmt: on


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('real_position', sa.Integer(), nullable=True))
    op.add_column('schedule', sa.Column('skip', sa.Boolean(), server_default='False', nullable=True))
    op.create_unique_constraint(op.f('uq_schedule_real_position'), 'schedule', ['real_position'], deferrable=True)
    op.drop_constraint(op.f('uq_schedule_position'), 'schedule', type_='unique')
    op.create_unique_constraint(op.f('uq_schedule_position'), 'schedule', ['position'], deferrable=True)
    op.drop_column('schedule', 'hidden')
    op.execute(create_function)
    op.execute(create_trigger)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_trigger)
    op.execute(drop_function)
    op.add_column('schedule', sa.Column('hidden', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('uq_schedule_real_position'), 'schedule', type_='unique')
    op.drop_constraint(op.f('uq_schedule_position'), 'schedule', type_='unique')
    op.create_unique_constraint(op.f('uq_schedule_position'), 'schedule', ['position'])
    op.drop_column('schedule', 'skip')
    op.drop_column('schedule', 'real_position')
    # ### end Alembic commands ###
