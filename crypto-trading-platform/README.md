# Crypto Futures Quant Trading Platform

A modular, event-driven cryptocurrency futures trading workstation for **quant research, backtesting, and (future) live execution**.

> Note: This repository currently contains a working backtest loop with a mock execution outcome (win/loss is randomized for demonstration), plus a real risk-manager gate (daily drawdown + consecutive losses).

---

## What’s implemented (current repo behavior)

### Strategy engine
- Strategies must implement `backend/strategies/base.py`:
  - `on_tick(tick_data)`
  - `on_orderbook(orderbook_data)`
  - `generate_signal()`
- `backend/engine/manager.py::StrategyManager` routes market data to **active strategies**.

### 3-way strategy mode switch (matches `StrategyManager`)
Configured via `StrategyManager.set_mode(mode, selected_strategy_names=None)`:
- **MODE_SINGLE (1)**: exactly one strategy by name
- **MODE_ALL (2)**: run all available strategies
- **MODE_MULTIPLE (3)**: run a provided subset of strategy names

### Risk management gate (matches `RiskManager`)
`backend/execution/risk_manager.py::RiskManager` enforces:
- **Daily drawdown limit**: reject new signals when `daily_drawdown >= max_daily_drawdown_pct`
- **Tilt / consecutive losses**: reject new signals when `consecutive_losses >= max_consecutive_losses`

It also contains a position sizing helper for live execution paths:
- `calculate_position_size(entry_price, stop_loss)` sizes to risk `max_risk_pct` of total equity.

### Backtest execution
`backend/engine/backtest_engine.py::BacktestEngine`:
1. Feeds each tick to active strategies (`on_tick`)
2. Polls each strategy for `generate_signal()`
3. If a signal is a dict, it must pass `risk_manager.evaluate_signal(signal)` to be executed
4. Executes via mock/immediate resolution:
   - win/loss outcome is randomized
   - profit/loss is applied as % of `total_equity`

---

## Implemented strategies

This repo provides multiple strategy implementations under `crypto-trading-platform/backend/strategies/`, including (names used by `run_backtest.py`):
- `KalmanPairs`
- `VPINToxicity`
- `PCANeutral`
- `MeanReversion`
- `HMMRegime`
- `IVCrush`
- `DispersionArb`
- `OrderFlowScalping`

---

## Running the project

### Run the backtester
Uses a built-in mock price series (random walk):

```bash
python run_backtest.py
```

By default, `run_backtest.py` configures the engine to run **all strategies**:
- `engine.set_mode(StrategyManager.MODE_ALL)`

### Run unit tests
```bash
python -m pytest backend/tests/
```

---

## How the backtest loop works (high level)

For each tick in the provided `data_feed`:
1. `StrategyManager.route_tick(tick)` calls `strategy.on_tick(tick)` for every active strategy.
2. `StrategyManager.poll_signals()` collects `strategy.generate_signal()`.
3. For each dict signal:
   - `RiskManager.evaluate_signal(signal)` decides whether trading is allowed.
   - If approved, `BacktestEngine._simulate_execution(...)` updates equity and stores a trade record.

At the end, the engine prints:
- total trades
- win rate (based on randomized outcomes)
- final equity
- max consecutive losses reached

---

## Folder layout (relevant parts)

```
crypto-trading-platform/
├─ backend/
│  ├─ core/
│  │  └─ events.py
│  ├─ data/
│  │  └─ feed.py
│  ├─ engine/
│  │  ├─ backtest_engine.py
│  │  ├─ live_engine.py
│  │  └─ manager.py
│  ├─ execution/
│  │  ├─ executor.py
│  │  └─ risk_manager.py
│  ├─ strategies/
│  │  ├─ base.py
│  │  └─ *.py
│  └─ tests/
│     └─ backend/tests/*
├─ run_backtest.py
└─ tui/
   └─ app.py
```

---

## Future / recommended architecture (vision)

The README used to describe a full production-ready, microservices/event-bus + web dashboard architecture. That vision is still a useful roadmap, but it is **not required** to run the current backtest.

Recommended next steps:
- Replace mock execution in `BacktestEngine` with position lifecycle + mark-to-market against future ticks (or simulated order matching).
- Wire `LiveEngine` to a real/exchange adapter via `Executor`.
- Add real market data feeds and event serialization.
- Expand the TUI and (if desired) add a web dashboard.

