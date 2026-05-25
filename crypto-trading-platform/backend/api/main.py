from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict, Any
import asyncio
import json
from ..data.database import get_db
from ..data.models import TradeLog, BacktestRun
from sqlalchemy.orm import Session

app = FastAPI(title="Crypto Quant Trading Platform API")

# Simple memory-based connection manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        data = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(data)
            except Exception:
                pass

manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"status": "Live Engine API Running"}

@app.get("/api/backtests")
def get_backtest_runs(db: Session = Depends(get_db)):
    """Retrieve historical backtest summary runs."""
    runs = db.query(BacktestRun).order_by(BacktestRun.id.desc()).limit(10).all()
    return runs

@app.get("/api/backtests/{run_id}/trades")
def get_backtest_trades(run_id: int, db: Session = Depends(get_db)):
    """Retrieve trades for a specific run (mocked to just get latest trades for MVP)."""
    # In a full implementation, TradeLog would have a run_id foreign key.
    trades = db.query(TradeLog).order_by(TradeLog.id.desc()).limit(50).all()
    return trades

@app.websocket("/ws/market_data")
async def websocket_endpoint(websocket: WebSocket):
    """
    Frontend can connect here to receive live ticks, orderbook updates, and position states.
    """
    await manager.connect(websocket)
    try:
        # Mock broadcasting state from the engine.
        # In a real app, the LiveEngine would emit events to an asyncio Queue or Redis channel that this task consumes.
        while True:
            # Check for commands
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=2.0)
            except asyncio.TimeoutError:
                data = None

            # Broadcast mock state simulating the engine
            await manager.broadcast({
                "type": "orderbook_update",
                "symbol": "BTC/USDT",
                "best_bid": 65000.0,
                "best_ask": 65001.0
            })

            await asyncio.sleep(1) # Broadcast every 1s
    except WebSocketDisconnect:
        manager.disconnect(websocket)
