import ccxt
import time
from typing import Dict, Any, Optional
from structlog import get_logger
from ..core.config import settings

logger = get_logger()


class LiveExecutor:
    """
    Executes actual orders on an exchange via CCXT with order confirmation and position sync.
    """
    def __init__(self, exchange_id: Optional[str] = None, api_key: Optional[str] = None,
                 secret: Optional[str] = None, testnet: Optional[bool] = None):
        exchange_id = exchange_id or settings.exchange_id
        api_key = api_key or settings.api_key
        secret = secret or settings.api_secret
        testnet = testnet if testnet is not None else settings.testnet

        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
        })

        if testnet:
            self.exchange.set_sandbox_mode(True)

        self._pending_orders: Dict[str, Dict[str, Any]] = {}

    def submit_order(self, symbol: str, side: str, order_type: str,
                     quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
        try:
            logger.info("order_submit", symbol=symbol, side=side, type=order_type, qty=quantity)
            if order_type.lower() == 'market':
                order = self.exchange.create_market_order(symbol, side.lower(), quantity)
            elif order_type.lower() == 'limit':
                order = self.exchange.create_limit_order(symbol, side.lower(), quantity, price)
            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            self._pending_orders[order.get('id', '')] = {
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'submitted_at': time.time(),
                'order': order,
            }
            return order
        except Exception as e:
            logger.error("order_failed", symbol=symbol, error=str(e))
            return {"status": "failed", "error": str(e)}

    def confirm_order(self, order_id: str, timeout: float = 10.0) -> Optional[Dict[str, Any]]:
        """Poll exchange until order is filled or timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                order = self.exchange.fetch_order(order_id, self._pending_orders[order_id]['symbol'])
                if order.get('status') == 'closed' or order.get('filled', 0) > 0:
                    logger.info("order_confirmed", order_id=order_id, filled=order.get('filled'))
                    return order
            except Exception:
                pass
            time.sleep(0.5)
        logger.warning("order_timeout", order_id=order_id)
        return None

    def fetch_positions(self, symbol: Optional[str] = None) -> list:
        """Fetch current open positions from the exchange."""
        try:
            positions = self.exchange.fetch_positions([symbol] if symbol else [])
            return positions
        except Exception as e:
            logger.error("fetch_positions_failed", error=str(e))
            return []

    def submit_reduce_only_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        try:
            logger.info("reduce_only_order", symbol=symbol, side=side, qty=quantity)
            order = self.exchange.create_order(symbol, "market", side.lower(), quantity, params={'reduceOnly': True})
            return order
        except Exception as e:
            logger.error("reduce_only_failed", error=str(e))
            return {"status": "failed", "error": str(e)}

    def cancel_order(self, order_id: str, symbol: str):
        try:
            return self.exchange.cancel_order(order_id, symbol)
        except Exception as e:
            logger.warning("cancel_failed", order_id=order_id, error=str(e))
            return None
