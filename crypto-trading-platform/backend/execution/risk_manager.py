from typing import Dict, Any

class RiskManager:
    """
    Handles position sizing and risk limits to prevent ruin.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.max_risk_per_trade = self.config.get("max_risk_pct", 0.01)
        self.max_consecutive_losses = self.config.get("max_consecutive_losses", 3)
        self.max_daily_drawdown_pct = self.config.get("max_daily_drawdown_pct", 0.05)

        self.consecutive_losses = 0
        self.daily_drawdown = 0.0
        self.total_equity = self.config.get("starting_equity", 10000.0)
        self.peak_equity = self.total_equity
        self.tick_counter = 0
        self.suppress_log = False

    def evaluate_signal(self, signal: Dict[str, Any]) -> bool:
        if self.total_equity <= 0:
            return False
        if self.daily_drawdown >= self.max_daily_drawdown_pct:
            if not self.suppress_log:
                print("RISK REJECT: Daily drawdown limit reached.")
                self.suppress_log = True
            return False
        if self.consecutive_losses >= self.max_consecutive_losses:
            if not self.suppress_log:
                print(f"RISK REJECT: {self.consecutive_losses} consecutive losses. Cooling down.")
                self.suppress_log = True
            return False
        return True

    def calculate_position_size(self, entry_price: float, stop_loss: float) -> float:
        if entry_price == stop_loss:
            return 0.0
        max_notional_pct = self.config.get("max_position_pct", 0.20)
        risk_amount = self.total_equity * self.max_risk_per_trade
        price_risk_per_unit = abs(entry_price - stop_loss)
        size_from_risk = risk_amount / price_risk_per_unit
        max_size_from_notional = (self.total_equity * max_notional_pct) / entry_price
        return min(size_from_risk, max_size_from_notional)

    def update_trade_result(self, pnl: float):
        self.tick_counter += 1
        self.total_equity += pnl
        if self.total_equity > self.peak_equity:
            self.peak_equity = self.total_equity

        if pnl < 0:
            self.consecutive_losses += 1
            current_drawdown = (self.peak_equity - self.total_equity) / self.peak_equity
            self.daily_drawdown = max(self.daily_drawdown, current_drawdown)
        else:
            self.consecutive_losses = 0

        if self.tick_counter % 24 == 0:
            self.daily_drawdown *= 0.5
            self.suppress_log = False
