# Crypto Futures Quant Trading Platform

A full-stack, institutional-grade cryptocurrency futures trading platform designed for quantitative strategy research, order-flow analysis, backtesting, and live execution.

## System Architecture

The platform features a highly modular, event-driven, microservices-oriented architecture allowing multiple autonomous strategies to run concurrently. It is split into:
- **Backend**: Python-based (FastAPI/asyncio) handling data ingestion, the strategy engine, risk management, and order execution.
- **Frontend**: A Next.js/React web dashboard and a Python-based Terminal UI (TUI) for power users.

## The Strategy Engine (3-Way Switch)

The core `StrategyManager` utilizes a 3-way switch mechanism, allowing the user to seamlessly toggle how the platform operates:
1. **Single Strategy Mode**: Focus all capital and data routing into one specific strategy.
2. **All Strategies Mode**: Runs all available strategies simultaneously for maximum market coverage.
3. **Multiple Strategies Mode**: Run a custom subset (e.g., only running the mean reversion and scalping strategies).

## Implemented Strategies

The platform currently includes 8 highly advanced quantitative frameworks:

1. **Kalman Filter Pairs Trading**: Dynamically adjusts hedge ratios between highly correlated crypto assets (e.g., BTC vs ETH) without fixed rolling windows.
2. **VPIN Toxicity Model**: Analyzes order flow toxicity using volume buckets instead of time to detect structural market stress and predict liquidations.
3. **PCA Factor Neutral Long/Short**: Uses Principal Component Analysis to neutralize broad market beta, trading pure idiosyncratic alpha.
4. **Cross-Sectional Mean Reversion**: Capitalizes on narrative-driven pumps and dumps by fading massive standard deviation outliers relative to their peer sectors.
5. **Hidden Markov Regime Detection**: Detects unobservable macro state shifts (bull expansion, bear capitulation, range) to algorithmically toggle sub-strategies.
6. **Earnings Implied Volatility Crush**: Exploits scheduled macro events (CPI, FOMC, forks) by shorting volatility just prior to the event to capture the premium collapse.
7. **Dispersion Volatility Arbitrage**: Exploits the correlation spread between a broad crypto index and its individual underlying token constituents.
8. **Order Flow Scalping AI**: A high-frequency strategy executing strictly on footprint absorption, delta divergence, and stacked imbalances with a strict minimum confidence threshold.

## Risk Management Module

To prevent ruin during live and paper trading, the platform enforces strict, globally managed risk limits through the `RiskManager`:
- **Position Sizing**: Dynamically sizes trades to risk a maximum of 1% of total equity per trade.
- **Tilt Protection**: Automatically halts execution if a strategy hits a maximum of 3 consecutive losses.
- **Daily Drawdown Limits**: Halts the entire system if the global portfolio drops below a 5% daily maximum drawdown threshold.

## Running the Project

### Running the Backtester
You can simulate the execution of all 8 strategies using the built-in mock data generator:
```bash
python run_backtest.py
```

### Running Unit Tests
The project features a suite of tests validating the event models, strategy initializations, the 3-way switch manager, and the risk management engine.
```bash
python -m pytest backend/tests/
```
