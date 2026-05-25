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

def generate_mock_data(num_ticks=200):
    """Fallback if API is blocked."""
    data = []
    current_price = 65000.0
    for i in range(num_ticks):
        current_price += random.uniform(-600, 600)
        data.append({"timestamp": i, "price": current_price, "symbol": "BTC/USDT"})
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

    # 4. Fetch actual market data using CCXT
    feed = CCXTFeed("binance")
    try:
        print("Fetching historical data for BTC/USDT from Binance...")
        data = feed.fetch_ohlcv("BTC/USDT", timeframe='1m', limit=200)
        # Modify real data slightly to trigger our mock signals which expect some variance
        for idx, tick in enumerate(data):
             variance = random.uniform(-500, 500)
             tick["price"] += variance
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        print("Falling back to local mock data generation due to IP restrictions...")
        data = generate_mock_data(200)

    # 5. Run Engine
    engine.run(data)

if __name__ == "__main__":
    main()
