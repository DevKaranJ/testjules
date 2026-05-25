import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.engine.manager import StrategyManager
from backend.strategies.base import Strategy

class DummyStrategy(Strategy):
    def on_tick(self, tick_data):
        pass
    def on_orderbook(self, orderbook_data):
        pass
    def generate_signal(self):
        return {"action": "TEST"}

def test_strategy_manager_switch():
    s1 = DummyStrategy()
    s2 = DummyStrategy()
    s3 = DummyStrategy()

    available = {
        "strat1": s1,
        "strat2": s2,
        "strat3": s3
    }

    manager = StrategyManager(available)

    # Test Option 1: Single
    manager.set_mode(StrategyManager.MODE_SINGLE, ["strat1"])
    assert len(manager.active_strategies) == 1
    assert "strat1" in manager.active_strategies

    # Test Option 2: All
    manager.set_mode(StrategyManager.MODE_ALL)
    assert len(manager.active_strategies) == 3
    assert "strat2" in manager.active_strategies

    # Test Option 3: Multiple
    manager.set_mode(StrategyManager.MODE_MULTIPLE, ["strat1", "strat3"])
    assert len(manager.active_strategies) == 2
    assert "strat1" in manager.active_strategies
    assert "strat3" in manager.active_strategies
    assert "strat2" not in manager.active_strategies

    # Error checking
    with pytest.raises(ValueError):
         manager.set_mode(StrategyManager.MODE_SINGLE, ["strat1", "strat2"])
