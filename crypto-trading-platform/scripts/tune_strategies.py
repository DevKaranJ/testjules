"""
Parameter sweep script for strategy tuning.

Usage:
    python scripts/tune_strategies.py --strategy MeanReversion --param deviation --values 1.0 1.5 2.0 2.5 3.0
    python scripts/tune_strategies.py --strategy KalmanPairs --param z_score_threshold --values 1.5 2.0 2.5
    python scripts/tune_strategies.py --all --ticks 100
"""
import argparse
import sys
from typing import Dict, Any

sys.path.insert(0, ".")

from backend.strategies.base import Strategy
from backend.strategies.mean_reversion import MeanReversionStrategy
from backend.strategies.kalman_pairs import KalmanPairsStrategy
from backend.strategies.hmm_regime import HMMRegimeStrategy
from backend.strategies.iv_crush import IVCrushStrategy
from backend.strategies.orderflow_scalping import OrderFlowScalpingStrategy
from backend.strategies.dispersion_arb import DispersionArbitrageStrategy as DispersionArbStrategy
from backend.strategies.pca_neutral import PCANeutralStrategy
from backend.strategies.vpin_toxicity import VPINToxicityStrategy
from backend.engine.backtest_engine import BacktestEngine
from backend.engine.manager import StrategyManager
from backend.strategies.config import STRATEGY_CONFIG_MAP
from backend.core.config import settings

import numpy as np

STRATEGY_CLASSES = {
    "MeanReversion": MeanReversionStrategy,
    "KalmanPairs": KalmanPairsStrategy,
    "HMMRegime": HMMRegimeStrategy,
    "IVCrush": IVCrushStrategy,
    "OrderFlowScalping": OrderFlowScalpingStrategy,
    "DispersionArb": DispersionArbStrategy,
    "PCANeutral": PCANeutralStrategy,
    "VPINToxicity": VPINToxicityStrategy,
}


def generate_synthetic_data(ticks: int = 100, start_price: float = 70000.0, volatility: float = 0.02) -> list:
    """Generate synthetic price data with drift and mean reversion."""
    data = []
    price = start_price
    for i in range(ticks):
        drift = 0.0001
        shock = np.random.normal(0, volatility)
        price = price * (1 + drift + shock)
        data.append({
            "price": round(price, 2),
            "symbol": "BTC/USDT",
            "timestamp": i,
            "bid": round(price - 0.5, 2),
            "ask": round(price + 0.5, 2),
        })
    return data


def run_single_backtest(strategy_name: str, params: Dict[str, Any], ticks: int = 100) -> Dict[str, Any]:
    """Run a backtest with specified strategy parameters and return results."""
    cls = STRATEGY_CLASSES[strategy_name]
    strategy = cls(config=params)
    engine = BacktestEngine(
        {strategy_name: strategy},
        {
            "starting_equity": settings.starting_equity,
            "max_risk_pct": settings.max_risk_pct,
            "max_consecutive_losses": settings.max_consecutive_losses,
            "max_daily_drawdown_pct": settings.max_daily_drawdown_pct,
        },
    )
    engine.set_mode(StrategyManager.MODE_ALL)
    data = generate_synthetic_data(ticks)
    engine.run(data)
    win_rate = (engine.winning_trades / engine.total_trades * 100) if engine.total_trades > 0 else 0.0
    return {
        "strategy": strategy_name,
        "params": params,
        "total_trades": engine.total_trades,
        "win_rate": round(win_rate, 1),
        "final_equity": round(engine.risk_manager.total_equity, 2),
        "return_pct": round((engine.risk_manager.total_equity - engine.start_equity) / engine.start_equity * 100, 2),
    }


def sweep_parameter(strategy_name: str, param_name: str, values: list, ticks: int = 100):
    """Sweep a single parameter and report results."""
    print(f"\n=== Sweeping {strategy_name}.{param_name} ===")
    print(f"{'Value':>10} | {'Trades':>6} | {'WinRate':>7} | {'Return':>8} | {'FinalEquity':>12}")
    print("-" * 52)
    for val in values:
        result = run_single_backtest(strategy_name, {param_name: val}, ticks=ticks)
        print(
            f"{str(val):>10} | {result['total_trades']:>6} | {result['win_rate']:>6}% | "
            f"{result['return_pct']:>7}% | ${result['final_equity']:>9,.2f}"
        )


def run_all_defaults(ticks: int = 100):
    """Run each strategy with default params and report results."""
    print(f"\n=== All Strategies (default params, {ticks} ticks) ===")
    print(f"{'Strategy':>18} | {'Trades':>6} | {'WinRate':>7} | {'Return':>8} | {'FinalEquity':>12}")
    print("-" * 58)
    for name in STRATEGY_CLASSES:
        cfg_cls = STRATEGY_CONFIG_MAP[name]
        params = cfg_cls().model_dump()
        result = run_single_backtest(name, params, ticks=ticks)
        print(
            f"{name:>18} | {result['total_trades']:>6} | {result['win_rate']:>6}% | "
            f"{result['return_pct']:>7}% | ${result['final_equity']:>9,.2f}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Strategy parameter tuner")
    parser.add_argument("--strategy", type=str, help="Strategy name to tune")
    parser.add_argument("--param", type=str, help="Parameter name to sweep")
    parser.add_argument("--values", type=float, nargs="+", help="Parameter values to test")
    parser.add_argument("--all", action="store_true", help="Run all strategies with defaults")
    parser.add_argument("--ticks", type=int, default=100, help="Number of synthetic data points")
    args = parser.parse_args()

    if args.all:
        run_all_defaults(ticks=args.ticks)
    elif args.strategy and args.param and args.values:
        sweep_parameter(args.strategy, args.param, args.values, ticks=args.ticks)
    else:
        parser.print_help()
