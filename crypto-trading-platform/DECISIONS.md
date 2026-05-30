# Architecture Decisions Log

**Decision 1: Event-Driven Architecture**
- *Context*: Need low latency and decoupled strategy execution.
- *Decision*: Pass standardized `MarketEvent` and `SignalEvent` dataclasses between components.

**Decision 2: 3-Way Strategy Switch**
- *Context*: User wants flexibility in testing.
- *Decision*: Implemented `StrategyManager` supporting `MODE_SINGLE`, `MODE_ALL`, and `MODE_MULTIPLE` to dynamically route ticks.

**Decision 3: Database Selection**
- *Context*: Need persistence for trade logs but easy local development.
- *Decision*: Used SQLAlchemy. Configured `sqlite:///` for default local dev, and `postgresql://` via environment variables for Docker production.

**Decision 4: Frontend Framework**
- *Context*: Need a high-performance quant dashboard.
- *Decision*: Next.js 14 (App Router) + Zustand for state + Lightweight Charts for rendering live WebSocket data.

**Decision 5: Execution Simulation**
- *Context*: Need realistic backtests.
- *Decision*: Implemented `PositionManager` to track trades over time (instead of instant mocking) and added `FeeModel` and `SlippageModel`.

**Decision 6: Abstract Execution Layer**
- *Context*: Backtesting and live trading need the same signal pipeline but different order execution.
- *Decision*: Abstract `Executor` base class with inline simulation (backtest) and `LiveExecutor` (CCXT API calls).

**Decision 7: RiskManager as Signal Gate**
- *Context*: Risk controls must be enforced before any position is opened.
- *Decision*: PositionManager only receives signals that pass `RiskManager.evaluate_signal()`.

**Decision 8: Zustand + WebSocket State**
- *Context*: Frontend needs real-time market data without polling.
- *Decision*: Zustand store with embedded WebSocket connection parsing `orderbook_update` messages.

**Decision 9: lightweight-charts**
- *Context*: Need financial charting with candlestick support.
- *Decision*: TradingView's lightweight-charts library (free, no license key for basic use).

**Decision 10: Textual for TUI**
- *Context*: Terminal-based UI alternative to web dashboard.
- *Decision*: Textual framework (Python) for TUI with DataTable and Log widgets.
