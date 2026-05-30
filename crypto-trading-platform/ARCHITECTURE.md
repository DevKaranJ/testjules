# Architecture

Please refer to `DESIGN.md` for the comprehensive original architectural vision and `FRONTEND_DESIGN.md` for UI specifications.

**High-Level Flow:**
1. **Data Feed:** `CCXTFeed` (historical) or `CCXTProFeed` (live WebSockets) ingests data into `MarketEvent`s.
2. **Strategy Manager:** Routes events to the 8 quant strategies.
3. **Strategies:** Use numpy/scipy to generate `SignalEvent`s (LONG/SHORT/CLOSE).
4. **Risk Manager:** Intercepts signals, evaluates daily drawdown, computes 1% position sizing.
5. **Position Manager & Executor:** Tracks open trades, applies simulated slippage/fees (in Backtest mode), or executes real trades via `LiveExecutor`.
6. **API Layer:** FastAPI server broadcasts trade logs and state to connected WebSocket clients.
7. **Frontend:** React Dashboard and Python TUI consume the API to display the active state.

---

## Detailed Architecture

```
                          ┌─────────────────────────────┐
                          │      run_backtest.py         │
                          │   (entry-point / CLI)        │
                          └──────────┬──────────────────┘
                                     │
                          ┌──────────▼──────────────────┐
                          │      StrategyManager         │
                          │  (MODE_SINGLE/ALL/MULTIPLE)  │
                          └──────────┬──────────────────┘
                                     │ routes ticks/orderbooks
                    ┌────────────────┼────────────────┐
                    │                │                │
         ┌──────────▼──────┐  ┌─────▼──────┐  ┌──────▼──────────┐
         │   BacktestEngine │  │ LiveEngine  │  │   Strategies    │
         │  (simulation)    │  │ (live/paper)│  │  (×8 concrete)  │
         └──────────┬──────┘  └──────┬──────┘  └─────────────────┘
                    │                │
         ┌──────────▼────────────────▼──────────┐
         │         Execution Layer               │
         │  RiskManager → PositionManager →      │
         │  FeeModel / SlippageModel → Executor  │
         └──────────┬────────────────┬───────────┘
                    │                │
         ┌──────────▼──┐     ┌──────▼───────────┐
         │  Backtest   │     │  LiveExecutor    │
         │  Executor   │     │  (CCXT orders)   │
         └─────────────┘     └──────┬───────────┘
                                    │
         ┌──────────────────────────▼───────────────┐
         │          Data Layer                       │
         │  CCXTFeed (sync) / CCXTProFeed (async)    │
         │  → MarketEvent → Event System             │
         └──────────────────┬───────────────────────┘
                            │
         ┌──────────────────▼───────────────────────┐
         │          Persistence                      │
         │  SQLAlchemy → SQLite/PostgreSQL            │
         │  TradeLog, BacktestRun models              │
         └──────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend framework | FastAPI (Python 3.12) |
| API server | Uvicorn |
| Real-time | WebSocket (FastAPI native) |
| Database ORM | SQLAlchemy 2.0 |
| Database | SQLite (dev), PostgreSQL 15 (prod via Docker) |
| Data feeds | CCXT (sync REST), CCXT Pro (async WebSocket) |
| Backend testing | pytest |
| Frontend framework | Next.js 14 (React 18) |
| Frontend language | TypeScript 5 |
| Charts | lightweight-charts |
| State management | Zustand 5 |
| Styling | Tailwind CSS 4 |
| TUI framework | Textual |
| Containerization | Docker / Docker Compose |

## Strategy Architecture

All strategies inherit from `Strategy` ABC (`backend/strategies/base.py`):

```python
class Strategy(ABC):
    def __init__(self, config: Dict[str, Any]): ...
    @abstractmethod
    def on_tick(self, tick_data: Dict[str, Any]): ...
    @abstractmethod
    def on_orderbook(self, orderbook_data: Dict[str, Any]): ...
    @abstractmethod
    def generate_signal(self) -> Dict[str, Any]: ...
```

The StrategyManager supports 3 modes:
- **MODE_SINGLE (1)**: Run one named strategy
- **MODE_ALL (2)**: Run all strategies, poll all signals
- **MODE_MULTIPLE (3)**: Run a subset of named strategies

## Event System

Event dataclasses in `backend/core/events.py`:

| Event | Fields |
|-------|--------|
| `Event` | Base dataclass |
| `MarketEvent` | `symbol, price, volume, timestamp` |
| `SignalEvent` | `strategy_name, action, confidence, symbol, price` |
| `OrderEvent` | `symbol, order_type, quantity, price, side` |
| `FillEvent` | `symbol, quantity, fill_price, commission, order_id` |

## Key Design Decisions

1. **Strategy ABC pattern**: All strategies share the same interface, enabling the 3-way switch
2. **Event-driven architecture**: MarketEvent → SignalEvent → OrderEvent → FillEvent pipeline
3. **Abstracted execution**: Backtest vs Live execution swapped transparently
4. **ORM persistence**: SQLAlchemy for both SQLite (dev) and PostgreSQL (prod)
5. **Separation of concerns**: RiskManager evaluates signals before PositionManager executes
