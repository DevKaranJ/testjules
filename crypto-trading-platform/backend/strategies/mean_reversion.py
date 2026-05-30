from .base import Strategy
from typing import Dict, Any
import numpy as np
from collections import defaultdict

class MeanReversionStrategy(Strategy):
    """
    4. Cross-Sectional Mean Reversion Engine
    Identifies massive deviations in asset performance relative to their peer group
    and fades the outliers using z-score ranking.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.deviation_threshold = self.config.get("deviation", 2.0)
        self.lookback = self.config.get("lookback", 20)
        self.prices: Dict[str, list] = defaultdict(list)

    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        sym = tick_data["symbol"]
        self.prices[sym].append(tick_data["price"])
        if len(self.prices[sym]) > self.lookback + 1:
            self.prices[sym].pop(0)

    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        pass

    def generate_signal(self) -> Any:
        valid = {sym: p for sym, p in self.prices.items() if len(p) >= self.lookback}
        if len(valid) < 2:
            return "NO TRADE — insufficient assets for cross-sectional comparison."

        returns = {}
        for sym, prices in valid.items():
            ret = (prices[-1] - prices[0]) / prices[0]
            returns[sym] = ret

        ret_array = np.array(list(returns.values()))
        mean_ret = np.mean(ret_array)
        std_ret = np.std(ret_array)

        if std_ret == 0:
            return "NO TRADE — no dispersion."

        max_z = 0.0
        target = None
        for sym, ret in returns.items():
            z = (ret - mean_ret) / std_ret
            if abs(z) > abs(max_z):
                max_z = z
                target = sym

        if abs(max_z) < self.deviation_threshold:
            return "NO TRADE — no significant deviations."

        direction = "SHORT" if max_z > 0 else "LONG"
        entry = self.prices[target][-1]
        return {
            "action": direction,
            "direction": direction,
            "symbol": target,
            "entry": entry,
            "stop_loss": entry * (0.97 if direction == "LONG" else 1.03),
            "take_profit": entry * (1.03 if direction == "LONG" else 0.97),
        }
