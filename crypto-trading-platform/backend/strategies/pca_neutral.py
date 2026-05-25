from .base import Strategy
from typing import Dict, Any
import numpy as np

class PCANeutralStrategy(Strategy):
    """
    3. PCA Factor Neutral Long/Short (Residual Exposure)
    Isolates pure idiosyncratic alpha by neutralizing market betas.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.lookback_days = self.config.get("lookback", 30)
        # Store historical prices for multiple assets
        self.prices_history: Dict[str, list] = {}

    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        sym = tick_data["symbol"]
        if sym not in self.prices_history:
            self.prices_history[sym] = []
        self.prices_history[sym].append(tick_data["price"])

        # Keep window bounded
        if len(self.prices_history[sym]) > self.lookback_days:
            self.prices_history[sym].pop(0)

    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        pass

    def generate_signal(self) -> Any:
        # Require at least two assets with sufficient history
        valid_assets = [sym for sym, prices in self.prices_history.items() if len(prices) >= 10]
        if len(valid_assets) < 2:
            return "NO TRADE — insufficient data for PCA."

        # Basic PCA proxy calculation using numpy (SVD)
        # In a real model, this would be computed on returns, not raw prices.
        matrix = []
        for sym in valid_assets:
            returns = np.diff(self.prices_history[sym][-10:]) / self.prices_history[sym][-10:-1]
            matrix.append(returns)

        try:
            X = np.array(matrix)
            # Center the data
            X_centered = X - np.mean(X, axis=1, keepdims=True)
            # Singular Value Decomposition as a proxy for PCA
            U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

            # Use the first principal component to identify the asset that deviates most
            pc1 = U[:, 0]
            max_deviation_idx = np.argmax(np.abs(pc1))
            target_asset = valid_assets[max_deviation_idx]

            # Simple mean reversion on the most deviating asset
            if pc1[max_deviation_idx] > 0:
                return {"action": "SHORT", "direction": "SHORT", "symbol": target_asset, "entry": self.prices_history[target_asset][-1]}
            else:
                return {"action": "LONG", "direction": "LONG", "symbol": target_asset, "entry": self.prices_history[target_asset][-1]}

        except Exception as e:
            return f"NO TRADE - computation error: {e}"
