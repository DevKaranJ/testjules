# Memory: Initial Repository Scan

**Date**: 2026-05-30
**Type**: Repository analysis
**Priority**: High

## What Was Learned

- This is a crypto futures quantitative trading platform
- Python/FastAPI backend + Next.js/React frontend + Textual TUI
- 8 trading strategies all implementing a common ABC
- 3-way strategy mode switch (single/all/multiple)
- Event-driven architecture (Market → Signal → Order → Fill)
- Backtesting and live trading share core execution code
- RiskManager gates signals before PositionManager executes
- Frontend uses Zustand + WebSocket for real-time data
- Tests use sys.path hacks (needs fixing)
- API keys hardcoded in live_executor.py (needs .env)

## Architecture Insights

1. The Strategy ABC is the central abstraction - all strategies, manager, and engines depend on it
2. The event pipeline is the backbone of communication between layers
3. BacktestEngine and LiveEngine share StrategyManager, RiskManager, PositionManager
4. Database models are simple (TradeLog, BacktestRun) with SQLAlchemy
5. CCXT is the sole exchange interface (data feeds + execution)

## Files Most Likely to Change

1. `backend/strategies/*.py` - adding new strategies
2. `backend/engine/backtest_engine.py` - improving simulation fidelity
3. `backend/execution/risk_manager.py` - adding risk rules
4. `frontend/src/components/*.tsx` - improving dashboard

## Gotchas

- `live_executor.py` has `__init__(exchange_id, api_key, secret, testnet)` - secrets hardcoded
- Tests all do `sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))` instead of proper install
- BacktestEngine uses `generate_mock_data()` - not connected to real exchange data for backtesting
- No database migrations - uses `Base.metadata.create_all()` on startup
- WebSocket broadcast runs as background task - no backpressure handling
