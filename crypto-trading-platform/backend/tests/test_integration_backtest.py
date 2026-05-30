import pytest
from backend.engine.backtest_engine import BacktestEngine
from backend.engine.manager import StrategyManager
from backend.strategies.base import Strategy
from backend.data.database import SessionLocal
from backend.data.models import BacktestRun, TradeLog


class DummyStrat(Strategy):
    def __init__(self, config=None):
        super().__init__(config)
        self._tick_count = 0

    def on_tick(self, tick_data):
        self._tick_count += 1

    def on_orderbook(self, orderbook_data):
        pass

    def generate_signal(self):
        if self._tick_count >= 3:
            self._tick_count = 0
            return {
                "direction": "LONG",
                "entry": 100.0,
                "stop_loss": 95.0,
                "take_profit": 110.0,
                "symbol": "BTC/USDT",
            }
        return "NO TRADE"


def make_tick(price: float, i: int) -> dict:
    return {
        "price": price,
        "symbol": "BTC/USDT",
        "timestamp": i,
        "bid": price - 0.5,
        "ask": price + 0.5,
    }


class TestBacktestEngine:
    def test_end_to_end_backtest(self):
        strategies = {"dummy": DummyStrat()}
        engine = BacktestEngine(strategies, {"starting_equity": 10000.0, "max_risk_pct": 0.01})
        engine.set_mode(StrategyManager.MODE_ALL)
        data = [make_tick(100.0, i) for i in range(20)]
        engine.run(data)
        assert engine.total_trades > 0
        assert engine.start_equity == 10000.0

    def test_results_saved_to_db(self):
        strategies = {"dummy2": DummyStrat()}
        engine = BacktestEngine(strategies, {"starting_equity": 50000.0, "max_risk_pct": 0.02})
        engine.set_mode(StrategyManager.MODE_ALL)
        data = [make_tick(200.0, i) for i in range(30)]
        engine.run(data)
        db = SessionLocal()
        try:
            runs = db.query(BacktestRun).order_by(BacktestRun.id.desc()).first()
            assert runs is not None
            assert runs.start_equity == 50000.0
            assert runs.total_trades > 0
            trades = db.query(TradeLog).filter(TradeLog.run_id == runs.id).all()
            assert len(trades) == runs.total_trades
            for t in trades:
                assert t.strategy_name == "dummy2"
                assert t.pnl != 0
        finally:
            db.close()

    def test_no_signals_no_trades(self):
        class NoOpStrat(Strategy):
            def on_tick(self, tick_data): pass
            def on_orderbook(self, orderbook_data): pass
            def generate_signal(self): return "NO TRADE"

        strategies = {"noop": NoOpStrat()}
        engine = BacktestEngine(strategies, {"starting_equity": 10000.0})
        engine.set_mode(StrategyManager.MODE_ALL)
        data = [make_tick(100.0, i) for i in range(10)]
        engine.run(data)
        assert engine.total_trades == 0
