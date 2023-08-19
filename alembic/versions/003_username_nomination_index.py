"""username_nomination_index

Revision ID: 003
Revises: 002
Create Date: 2023-08-19 23:56:43.628061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_nominations_title', 'nominations', type_='unique')
    op.create_index(op.f('ix_nominations_title'), 'nominations', ['title'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_nominations_title'), table_name='nominations')
    op.create_unique_constraint('uq_nominations_title', 'nominations', ['title'])
    # ### end Alembic commands ###
