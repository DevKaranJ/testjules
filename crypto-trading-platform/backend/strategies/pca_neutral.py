from .base import Strategy
from typing import Dict, Any

class PCANeutralStrategy(Strategy):
    """
    3. PCA Factor Neutral Long/Short (Residual Exposure)
    Isolates pure idiosyncratic alpha by neutralizing market betas (e.g. BTC/ETH drops)
    using Principal Component Analysis.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.lookback_days = self.config.get("lookback", 30)

    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        pass

    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        pass

    def generate_signal(self) -> Any:
        # Long top decile residuals, short bottom decile residuals
        return {"longs": [], "shorts": []}
