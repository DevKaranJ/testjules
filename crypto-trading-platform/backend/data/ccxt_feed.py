import ccxt
from typing import List, Dict, Any
from ..core.events import MarketEvent

class CCXTFeed:
    """
    Data feed adapter using the CCXT library.
    """
    def __init__(self, exchange_id: str = "binance"):
        self.exchange_id = exchange_id
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'enableRateLimit': True,
        })

    def fetch_ohlcv(self, symbol: str, timeframe: str = '1m', limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetches historical OHLCV data and converts to tick-like structures for the backtester.
        """
        raw_data = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        ticks = []

        for candle in raw_data:
            # timestamp, open, high, low, close, volume
            ticks.append({
                "timestamp": candle[0],
                "symbol": symbol,
                "price": candle[4], # Use close price as the simulated "tick" price
                "volume": candle[5]
            })

        return ticks

    def fetch_live_ticker(self, symbol: str) -> MarketEvent:
        """
        Fetches the current live ticker.
        (For real live trading, use CCXT Pro websockets instead).
        """
        ticker = self.exchange.fetch_ticker(symbol)

        return MarketEvent(
            symbol=symbol,
            data_type="tick",
            data={
                "timestamp": ticker['timestamp'],
                "price": ticker['last'],
                "volume": ticker['baseVolume']
            }
        )
