from typing import Dict, Any

class RiskManager:
    """
    Handles position sizing and risk limits to prevent ruin.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.max_risk_per_trade = self.config.get("max_risk_pct", 0.01) # Max 1% per trade
        self.max_consecutive_losses = self.config.get("max_consecutive_losses", 3)
        self.max_daily_drawdown_pct = self.config.get("max_daily_drawdown_pct", 0.05)

        # State tracking
        self.consecutive_losses = 0
        self.daily_drawdown = 0.0
        self.total_equity = self.config.get("starting_equity", 10000.0)

    def evaluate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        Evaluates a trading signal against global risk limits.
        Returns True if the signal is approved to trade, False otherwise.
        """
        # 1. Check drawdown
        if self.daily_drawdown >= self.max_daily_drawdown_pct:
            print("RISK REJECT: Daily drawdown limit reached.")
            return False

        # 2. Check consecutive losses (tilt protection)
        if self.consecutive_losses >= self.max_consecutive_losses:
            print("RISK REJECT: Max consecutive losses reached. Cooling down.")
            return False

        return True

    def calculate_position_size(self, entry_price: float, stop_loss: float) -> float:
        """
        Calculates position size based on 1% risk of total equity.
        """
        if entry_price == stop_loss:
            return 0.0

        risk_amount = self.total_equity * self.max_risk_per_trade
        price_risk_per_unit = abs(entry_price - stop_loss)

        return risk_amount / price_risk_per_unit

    def update_trade_result(self, pnl: float):
        """
        Updates the internal state based on a completed trade.
        """
        self.total_equity += pnl
        if pnl < 0:
            self.consecutive_losses += 1
            # Naive calculation for daily drawdown for simulation purposes
            self.daily_drawdown += abs(pnl / self.total_equity)
        else:
            self.consecutive_losses = 0
