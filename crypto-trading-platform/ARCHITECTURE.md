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