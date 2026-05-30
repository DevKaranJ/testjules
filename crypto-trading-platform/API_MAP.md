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