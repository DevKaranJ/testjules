import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.execution.models import FeeModel, SlippageModel
from backend.execution.position_manager import PositionManager

def test_fee_model():
    fee_model = FeeModel(maker_fee=0.0002, taker_fee=0.0005)
    # Price 100, Qty 10 -> Total value 1000
    # Maker fee: 1000 * 0.0002 = 0.2
    assert fee_model.calculate_fee(100.0, 10.0, is_maker=True) == 0.2
    # Taker fee: 1000 * 0.0005 = 0.5
    assert fee_model.calculate_fee(100.0, 10.0, is_maker=False) == 0.5

def test_position_manager_lifecycle():
    pm = PositionManager(FeeModel(0.000, 0.000), SlippageModel(0.0, 0.0))

    # Open long position
    # Entry 100, Stop Loss 90, Take Profit 110
    pm.open_position("TestStrat", "BTCUSDT", "LONG", 100.0, 1.0, 90.0, 110.0)
    assert len(pm.positions) == 1

    # Tick at 105 (no close)
    closed = pm.update({"price": 105.0, "symbol": "BTCUSDT"})
    assert len(closed) == 0
    assert len(pm.positions) == 1

    # Tick at 110 (take profit hit)
    closed = pm.update({"price": 110.0, "symbol": "BTCUSDT"})
    assert len(closed) == 1
    assert len(pm.positions) == 0

    # Validate PnL
    trade = closed[0]
    assert trade["net_pnl"] == 10.0
    assert trade["reason"] == "TAKE_PROFIT"
