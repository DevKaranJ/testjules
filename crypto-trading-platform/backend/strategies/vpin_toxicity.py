from .base import Strategy
from typing import Dict, Any

class VPINToxicityStrategy(Strategy):
    """
    2. Order Flow Toxicity Model (VPIN)
    Measures imbalance between buyers and sellers using volume buckets.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.bucket_size = self.config.get("bucket_size", 100) # e.g. BTC
        self.toxicity_threshold = self.config.get("toxicity_threshold", 0.90)

        self.current_bucket_vol = 0.0
        self.buy_vol = 0.0
        self.sell_vol = 0.0
        self.historical_vpin = []

    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        price = tick_data["price"]
        volume = tick_data.get("volume", 1.0)
        side = tick_data.get("side", "buy")

        # Accumulate volume
        self.current_bucket_vol += volume
        if side == "buy":
            self.buy_vol += volume
        else:
            self.sell_vol += volume

        # Check if bucket is filled
        if self.current_bucket_vol >= self.bucket_size:
            vpin = abs(self.buy_vol - self.sell_vol) / self.bucket_size
            self.historical_vpin.append(vpin)

            # Keep history bounded
            if len(self.historical_vpin) > 50:
                self.historical_vpin.pop(0)

            # Reset bucket
            self.current_bucket_vol = 0.0
            self.buy_vol = 0.0
            self.sell_vol = 0.0

    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        pass

    def generate_signal(self) -> Any:
        if not self.historical_vpin:
            return "NO TRADE — insufficient buckets."

        latest_vpin = self.historical_vpin[-1]

        if latest_vpin > self.toxicity_threshold:
            return {"action": "HALT_MARKET_MAKING", "reason": f"high_toxicity_{latest_vpin:.2f}", "direction": "NONE"}

        return "NO TRADE — normal conditions."
