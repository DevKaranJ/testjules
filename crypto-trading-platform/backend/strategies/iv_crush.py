from .base import Strategy
from typing import Dict, Any
import numpy as np

class IVCrushStrategy(Strategy):
    """
    6. Earnings Implied Volatility Crush
    Estimates implied volatility from price action and shorts when elevated
    relative to historical rank.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.iv_rank_threshold = self.config.get("iv_rank_threshold", 80.0)
        self.lookback = self.config.get("lookback", 100)
        self.prices = []

    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        self.prices.append(tick_data["price"])
        if len(self.prices) > self.lookback:
            self.prices.pop(0)

    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        pass

    def _estimate_iv(self) -> float:
        if len(self.prices) < 20:
            return 0.0
        returns = np.diff(self.prices) / self.prices[:-1]
        vol = np.std(returns) * np.sqrt(365 * 24 * 6)
        return vol * 100

    def _compute_iv_rank(self, iv: float) -> float:
        if len(self.prices) < 50:
            return 50.0
        historical_vols = []
        for i in range(10, len(self.prices), 10):
            segment = self.prices[i-10:i]
            if len(segment) >= 2:
                r = np.diff(segment) / segment[:-1]
                historical_vols.append(np.std(r) * np.sqrt(365 * 24 * 6) * 100)
        if not historical_vols:
            return 50.0
        return (sum(1 for v in historical_vols if v <= iv) / len(historical_vols)) * 100

    def generate_signal(self) -> Any:
        iv = self._estimate_iv()
        if iv == 0:
            return None
        iv_rank = self._compute_iv_rank(iv)
        if iv_rank > self.iv_rank_threshold and len(self.prices) >= 5:
            return {
                "action": "SHORT_VOLATILITY",
                "direction": "SHORT",
                "symbol": "BTC/USDT",
                "entry": self.prices[-1],
                "iv": iv,
                "iv_rank": iv_rank,
            }
        return None
