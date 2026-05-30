import sys
import os
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.engine.backtest_engine import BacktestEngine
from backend.engine.manager import StrategyManager
from backend.strategies.kalman_pairs import KalmanPairsStrategy
from backend.strategies.vpin_toxicity import VPINToxicityStrategy
from backend.strategies.pca_neutral import PCANeutralStrategy
from backend.strategies.mean_reversion import MeanReversionStrategy
from backend.strategies.hmm_regime import HMMRegimeStrategy
from backend.strategies.iv_crush import IVCrushStrategy
from backend.strategies.dispersion_arb import DispersionArbitrageStrategy
from backend.strategies.orderflow_scalping import OrderFlowScalpingStrategy
from backend.data.ccxt_feed import CCXTFeed

def fetch_historical_data(symbol="BTC/USDT", timeframe='1m', limit=200):
    """Fetch real market data from CCXT, with synthetic fallback."""
    feed = CCXTFeed("binance")
    try:
        print(f"Fetching {limit} {timeframe} candles for {symbol} from Binance...")
        data = feed.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if data and len(data) > 0:
            return data
    except Exception as e:
        print(f"CCXT fetch failed: {e}")

    print("Falling back to synthetic data with realistic regime structure...")
    data = []
    price = 65000.0
    import numpy as np
    for i in range(limit):
        drift = np.sin(i / 20) * 200
        noise = random.uniform(-300, 300)
        price += drift + noise
        data.append({"timestamp": i, "price": price, "symbol": symbol, "volume": random.uniform(10, 100)})
    return data

def main():
    # 1. Initialize all strategies
    strategies = {
        "KalmanPairs": KalmanPairsStrategy(),
        "VPINToxicity": VPINToxicityStrategy(),
        "PCANeutral": PCANeutralStrategy(),
        "MeanReversion": MeanReversionStrategy(),
        "HMMRegime": HMMRegimeStrategy(),
        "IVCrush": IVCrushStrategy(),
        "DispersionArb": DispersionArbitrageStrategy(),
        "OrderFlowScalping": OrderFlowScalpingStrategy()
    }

    # 2. Configure Risk
    risk_config = {
        "starting_equity": 100000.0,
        "max_risk_pct": 0.01,
        "max_consecutive_losses": 3,
        "max_daily_drawdown_pct": 0.05
    }

    # 3. Setup Backtester
    engine = BacktestEngine(strategies, risk_config)

    # Demonstrate the 3-Way Switch: Let's run all strategies
    print("Configuring Backtester for MODE_ALL...")
    engine.set_mode(StrategyManager.MODE_ALL)

    # 4. Fetch actual market data
    data = fetch_historical_data()

    # 5. Run Engine
    engine.run(data)

if __name__ == "__main__":
    main()
