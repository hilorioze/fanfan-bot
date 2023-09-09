"""quest

Revision ID: 007
Revises: 006
Create Date: 2023-09-09 23:59:06.400884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_achievements'))
    )
    op.create_table('received_achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('achievement_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], name=op.f('fk_received_achievements_achievement_id_achievements'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_received_achievements_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_received_achievements'))
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_user', sa.BigInteger(), nullable=False),
    sa.Column('to_user', sa.BigInteger(), nullable=False),
    sa.Column('points_added', sa.Integer(), nullable=True),
    sa.Column('achievement_added', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['achievement_added'], ['achievements.id'], name=op.f('fk_transactions_achievement_added_achievements'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['from_user'], ['users.id'], name=op.f('fk_transactions_from_user_users'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_user'], ['users.id'], name=op.f('fk_transactions_to_user_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_transactions'))
    )
    op.create_unique_constraint(op.f('uq_settings_id'), 'settings', ['id'])
    op.add_column('users', sa.Column('points', sa.Integer(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'points')
    op.drop_constraint(op.f('uq_settings_id'), 'settings', type_='unique')
    op.drop_table('transactions')
    op.drop_table('received_achievements')
    op.drop_table('achievements')
    # ### end Alembic commands ###
