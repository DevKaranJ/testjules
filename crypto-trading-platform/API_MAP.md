# API Map

This maps the endpoints exposed by the FastAPI server located in `backend/api/main.py`.

### REST Endpoints
- `GET /` : Health check. Returns `{"status": "Live Engine API Running"}`.
- `GET /api/backtests` : Retrieves a list of the 10 most recent Backtest Runs (from DB).
- `GET /api/backtests/{run_id}/trades` : Retrieves up to 50 recent trades for a specific run.

### WebSocket Endpoints
- `WS /ws/market_data` : The primary real-time socket.
  - *Client sends*: Commands (e.g. Subscribe to symbol).
  - *Server broadcasts*: Live orderbook updates, position state changes, and live chart ticks to all connected dashboards.

---

## Detailed API Reference

### FastAPI Backend (`backend/api/main.py`)

| Method | Path | Handler | Description | Auth |
|--------|------|---------|-------------|------|
| GET | `/` | `read_root()` | Health check | None |
| GET | `/api/backtests` | `get_backtest_runs()` | List saved backtest runs | None |
| GET | `/api/backtests/{run_id}/trades` | `get_backtest_trades(run_id)` | Get trades for a backtest run | None |
| WS | `/ws/market_data` | `websocket_endpoint()` | Real-time market data broadcasting | None |

### WebSocket Protocol

**Server → Client:**
```json
{"type": "orderbook_update", "data": {"symbol": "BTC/USDT", "bid": 50000.0, "ask": 50001.0}}
```

### ConnectionManager (`api/main.py:12`)
| Method | Description |
|--------|-------------|
| `connect(websocket)` | Accept and register WebSocket connection |
| `disconnect(websocket)` | Remove connection on disconnect |
| `broadcast(message)` | Send JSON message to all active connections |

### Frontend State API (`frontend/src/store/useStore.ts`)

```typescript
interface Trade { strategy: string; symbol: string; pnl: number }
interface PlatformState {
  trades: Trade[];
  prices: Record<string, number>;
  addTrade: (trade: Trade) => void;
  updatePrice: (symbol: string, price: number) => void;
}
```

### Internal Python APIs

| Module | Key Classes | Consumers |
|--------|-------------|-----------|
| `strategies/base.py` | `Strategy` (ABC) | All 8 strategies, StrategyManager |
| `engine/manager.py` | `StrategyManager` | BacktestEngine, LiveEngine |
| `execution/risk_manager.py` | `RiskManager` | BacktestEngine, LiveEngine |
| `execution/position_manager.py` | `PositionManager`, `Position` | BacktestEngine, LiveEngine |
| `execution/models.py` | `FeeModel`, `SlippageModel` | PositionManager, BacktestEngine |
| `execution/executor.py` | `Executor` (ABC) | BacktestEngine (inline) |
| `execution/live_executor.py` | `LiveExecutor` | LiveEngine |
| `data/feed.py` | `DataFeed` (ABC) | CCXTFeed, CCXTProFeed |
| `data/ccxt_feed.py` | `CCXTFeed` | run_backtest.py |
| `data/ccxt_pro_feed.py` | `CCXTProFeed` | LiveEngine |
| `data/models.py` | `TradeLog`, `BacktestRun` | BacktestEngine, LiveEngine, API |
| `data/database.py` | `SessionLocal`, `get_db` | BacktestEngine, LiveEngine, API, TUI |
