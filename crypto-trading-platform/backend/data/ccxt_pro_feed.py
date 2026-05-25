import ccxt.async_support as ccxtpro
import asyncio
from typing import Callable, Any
from ..core.events import MarketEvent

class CCXTProFeed:
    """
    Data feed adapter using the CCXT Pro library for WebSocket streaming.
    """
    def __init__(self, exchange_id: str = "binance"):
        self.exchange_id = exchange_id
        exchange_class = getattr(ccxtpro, exchange_id)
        self.exchange = exchange_class({
            'enableRateLimit': True,
        })
        self.running = False

    async def watch_ticker_loop(self, symbol: str, callback: Callable[[MarketEvent], None]):
        """
        Continuously watches live ticker via WebSockets.
        """
        self.running = True
        print(f"Connecting to {self.exchange_id} websocket for {symbol}...")
        try:
            while self.running:
                ticker = await self.exchange.watch_ticker(symbol)
                event = MarketEvent(
                    symbol=symbol,
                    data_type="tick",
                    data={
                        "timestamp": ticker['timestamp'],
                        "price": ticker['last'],
                        "volume": ticker['baseVolume']
                    }
                )
                callback(event)
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            await self.exchange.close()

    def stop(self):
        self.running = False
