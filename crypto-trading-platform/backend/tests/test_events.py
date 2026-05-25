import sys
import os

# Add project root to sys.path to allow correct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.core.events import MarketEvent, SignalEvent

def test_market_event():
    event = MarketEvent(symbol="BTC/USDT", data_type="tick", data={"price": 50000})
    assert event.symbol == "BTC/USDT"
    assert event.data["price"] == 50000

def test_signal_event():
    event = SignalEvent(strategy_id="Strat_1", symbol="BTC/USDT", side="buy", order_type="market", quantity=1.0)
    assert event.quantity == 1.0
    assert event.side == "buy"
