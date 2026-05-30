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