from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class TradeLog(Base):
    """
    Records an executed trade.
    """
    __tablename__ = 'trade_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_name = Column(String(50), nullable=False)
    symbol = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False) # LONG or SHORT
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    pnl = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)
    slippage = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class BacktestRun(Base):
    """
    Records the summary of a backtest execution.
    """
    __tablename__ = 'backtest_runs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_date = Column(DateTime, default=datetime.utcnow)
    strategies = Column(String(255)) # Comma separated list
    start_equity = Column(Float, nullable=False)
    end_equity = Column(Float, nullable=False)
    total_trades = Column(Integer, nullable=False)
    win_rate = Column(Float, nullable=False)
    max_drawdown = Column(Float, nullable=False)
    parameters = Column(JSON) # e.g., risk config


def init_db(engine):
    """Creates the tables in the database."""
    Base.metadata.create_all(engine)
