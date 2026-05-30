"""add_user_id_columns

Revision ID: 76c98572e94d
Revises: 544d53924b96
Create Date: 2026-05-30 13:12:38.085196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76c98572e94d'
down_revision: Union[str, Sequence[str], None] = '544d53924b96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('backtest_runs', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_backtest_runs_user_id'), 'backtest_runs', ['user_id'], unique=False)
    op.create_foreign_key('fk_backtest_runs_user_id', 'backtest_runs', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('trade_logs', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_trade_logs_user_id'), 'trade_logs', ['user_id'], unique=False)
    op.create_foreign_key('fk_trade_logs_user_id', 'trade_logs', 'users', ['user_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint('fk_trade_logs_user_id', 'trade_logs', type_='foreignkey')
    op.drop_index(op.f('ix_trade_logs_user_id'), table_name='trade_logs')
    op.drop_column('trade_logs', 'user_id')
    op.drop_constraint('fk_backtest_runs_user_id', 'backtest_runs', type_='foreignkey')
    op.drop_index(op.f('ix_backtest_runs_user_id'), table_name='backtest_runs')
    op.drop_column('backtest_runs', 'user_id')
