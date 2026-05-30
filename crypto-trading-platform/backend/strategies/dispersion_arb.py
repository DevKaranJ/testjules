from .base import Strategy
from typing import Dict, Any
from collections import defaultdict
import numpy as np

class DispersionArbitrageStrategy(Strategy):
    """
    7. Dispersion Volatility Arbitrage
    Computes pairwise rolling correlations among tracked assets and triggers
    dispersion trades when correlations collapse.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.correlation_threshold = self.config.get("correlation", 0.30)
        self.lookback = self.config.get("lookback", 50)
        self.prices: Dict[str, list] = defaultdict(list)

    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        sym = tick_data["symbol"]
        self.prices[sym].append(tick_data["price"])
        if len(self.prices[sym]) > self.lookback:
            self.prices[sym].pop(0)

    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        pass

    def generate_signal(self) -> Any:
        valid = {sym: p for sym, p in self.prices.items() if len(p) >= 30}
        if len(valid) < 2:
            return "NO TRADE — insufficient assets."

        symbols = list(valid.keys())
        returns = []
        min_len = min(len(valid[sym]) for sym in symbols)
        for sym in symbols:
            p = valid[sym][-min_len:]
            r = (np.array(p[1:]) - np.array(p[:-1])) / np.array(p[:-1])
            returns.append(r)

        ret_matrix = np.vstack(returns)
        corr_matrix = np.corrcoef(ret_matrix)
        triu_indices = np.triu_indices_from(corr_matrix, k=1)
        avg_corr = np.mean(corr_matrix[triu_indices])

        if avg_corr < self.correlation_threshold:
            return {
                "action": "ENTER_DISPERSION_TRADE",
                "direction": "SHORT",
                "symbol": symbols[0],
                "entry": valid[symbols[0]][-1],
                "avg_correlation": avg_corr,
            }
        return None
