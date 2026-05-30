from backend.execution.risk_manager import RiskManager

def test_risk_manager_position_sizing():
    rm = RiskManager({"starting_equity": 10000.0, "max_risk_pct": 0.01})
    # 1% of 10000 is 100
    # Entry 100, Stop Loss 90 -> risk per unit is 10
    # Size should be 10 units (10 * 10 = 100)
    size = rm.calculate_position_size(100.0, 90.0)
    assert size == 10.0

def test_risk_manager_consecutive_losses():
    rm = RiskManager({"max_consecutive_losses": 2})

    # Approve first trade
    assert rm.evaluate_signal({}) is True

    # 1st loss
    rm.update_trade_result(-100)
    assert rm.evaluate_signal({}) is True

    # 2nd loss
    rm.update_trade_result(-100)
    # Should be rejected now
    assert rm.evaluate_signal({}) is False

    # Reset on win
    rm.update_trade_result(500)
    assert rm.evaluate_signal({}) is True

def test_risk_manager_daily_drawdown():
    rm = RiskManager({"starting_equity": 1000.0, "max_daily_drawdown_pct": 0.10})

    rm.update_trade_result(-150) # 15% drawdown
    assert rm.evaluate_signal({}) is False
