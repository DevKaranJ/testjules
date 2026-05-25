import ccxt
from typing import Dict, Any

class LiveExecutor:
    """
    Executes actual orders on an exchange via CCXT.
    """
    def __init__(self, exchange_id: str, api_key: str, secret: str, testnet: bool = True):
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
        })

        if testnet:
            self.exchange.set_sandbox_mode(True)

    def submit_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> Dict[str, Any]:
        """
        Submits a live order to the configured exchange.
        """
        try:
            print(f"Submitting {order_type} {side} order for {quantity} {symbol} at {price}")
            if order_type.lower() == 'market':
                order = self.exchange.create_market_order(symbol, side, quantity)
            elif order_type.lower() == 'limit':
                order = self.exchange.create_limit_order(symbol, side, quantity, price)
            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            return order
        except Exception as e:
            print(f"Failed to submit order: {e}")
            return {"status": "failed", "error": str(e)}

    def submit_reduce_only_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Submits a market order strictly for closing positions, preventing accidental exposure flipping.
        """
        try:
            print(f"Submitting Reduce-Only {side} order for {quantity} {symbol}")
            # The exact param name varies slightly by exchange in CCXT. For Binance Futures it's usually 'reduceOnly'.
            order = self.exchange.create_order(symbol, "market", side, quantity, params={'reduceOnly': True})
            return order
        except Exception as e:
            print(f"Failed to submit reduce-only order: {e}")
            return {"status": "failed", "error": str(e)}

    def cancel_order(self, order_id: str, symbol: str):
        try:
            return self.exchange.cancel_order(order_id, symbol)
        except Exception as e:
            print(f"Failed to cancel order {order_id}: {e}")
            return None
