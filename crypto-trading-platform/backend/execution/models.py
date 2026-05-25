import random

class FeeModel:
    """
    Simulates exchange fee structures.
    """
    def __init__(self, maker_fee: float = 0.0002, taker_fee: float = 0.0005):
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee

    def calculate_fee(self, price: float, quantity: float, is_maker: bool = False) -> float:
        """
        Calculates the fee amount in quote currency.
        """
        fee_rate = self.maker_fee if is_maker else self.taker_fee
        return price * quantity * fee_rate


class SlippageModel:
    """
    Simulates order execution slippage.
    """
    def __init__(self, base_slippage_pct: float = 0.0005, volume_impact_multiplier: float = 0.1):
        self.base_slippage_pct = base_slippage_pct
        self.volume_impact_multiplier = volume_impact_multiplier

    def calculate_slippage(self, price: float, quantity: float, order_type: str = "market") -> float:
        """
        Calculates the absolute price difference caused by slippage.
        For limit orders, slippage is generally 0.
        """
        if order_type.lower() == "limit":
            return 0.0

        # Basic model: base slippage + a small random variance to simulate live market behavior
        variance = random.uniform(0.5, 1.5)
        # In a real model, we would factor in 'quantity' vs 'orderbook_depth'.
        # Here we mock a linear volume impact.
        total_slippage_pct = self.base_slippage_pct * variance * (1 + (quantity * self.volume_impact_multiplier))

        return price * total_slippage_pct
