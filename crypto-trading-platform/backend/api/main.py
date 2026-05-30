from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import asyncio
import json
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from structlog import get_logger

from ..data.database import get_db, check_db_connection
from ..data.models import TradeLog, BacktestRun
from ..core.config import settings
from ..core.logging import setup_logging
from ..core.schemas import (
    HealthResponse, StrategyListResponse, BacktestRunResponse,
    TradeLogResponse, PlatformStatus, ActionResponse,
)
from ..core.exceptions import StrategyNotFoundError

setup_logging()
logger = get_logger()


class ConnectionManager:
    def __init__(self, max_messages_per_sec: int = 10):
        self.active_connections: Dict[WebSocket, None] = {}
        self._rate_limit: Dict[str, float] = {}
        self._max_messages_per_sec = max_messages_per_sec

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        client_host = websocket.client.host if websocket.client else "unknown"
        self.active_connections[websocket] = None
        logger.info("ws_connected", client=client_host, total=len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.pop(websocket, None)
        client_host = websocket.client.host if websocket.client else "unknown"
        logger.info("ws_disconnected", client=client_host, total=len(self.active_connections))

    def check_rate_limit(self, websocket: WebSocket) -> bool:
        client_host = websocket.client.host if websocket.client else "unknown"
        now = asyncio.get_event_loop().time()
        last = self._rate_limit.get(client_host, 0)
        if now - last < 1.0 / self._max_messages_per_sec:
            logger.warning("ws_rate_limit_exceeded", client=client_host)
            return False
        self._rate_limit[client_host] = now
        return True

    async def broadcast(self, message: Dict[str, Any]):
        data = json.dumps(message, default=str)
        disconnected = []
        for conn in list(self.active_connections.keys()):
            try:
                await conn.send_text(data)
            except Exception:
                disconnected.append(conn)
        for conn in disconnected:
            try:
                self.disconnect(conn)
            except (ValueError, KeyError):
                pass


manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("api_starting", host=settings.api_host, port=settings.api_port)
    task = asyncio.create_task(_broadcast_market_state())
    yield
    task.cancel()
    logger.info("api_shutdown")


app = FastAPI(
    title="Crypto Quant Trading Platform API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("unhandled_exception", path=str(request.url), exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_code": "INTERNAL_ERROR"},
    )


@app.get("/", response_model=HealthResponse)
def read_root():
    return HealthResponse(status="ok", version="0.1.0", database=settings.database_url[:20])


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    db_ok = check_db_connection()
    return HealthResponse(
        status="ok" if db_ok else "degraded",
        version="0.1.0",
        database=settings.database_url[:20],
    )


@app.get("/api/backtests", response_model=List[BacktestRunResponse])
def get_backtest_runs(db: Session = Depends(get_db)):
    return db.query(BacktestRun).order_by(BacktestRun.id.desc()).limit(10).all()


@app.get("/api/backtests/{run_id}", response_model=BacktestRunResponse)
def get_backtest_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(BacktestRun).filter(BacktestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail=f"Backtest run {run_id} not found")
    return run


@app.get("/api/backtests/{run_id}/trades", response_model=List[TradeLogResponse])
def get_backtest_trades(run_id: int, db: Session = Depends(get_db)):
    trades = db.query(TradeLog).filter(TradeLog.run_id == run_id).order_by(TradeLog.id.desc()).limit(50).all()
    if not trades:
        trades = db.query(TradeLog).order_by(TradeLog.id.desc()).limit(50).all()
    return trades


strategy_status: Dict[str, str] = {
    "KalmanPairs": "stopped", "VPINToxicity": "stopped",
    "OrderFlowScalping": "stopped", "MeanReversion": "stopped",
    "HMMRegime": "stopped", "IVCrush": "stopped",
    "DispersionArb": "stopped", "PCANeutral": "stopped",
}


@app.get("/api/strategies", response_model=StrategyListResponse)
def get_strategies():
    return StrategyListResponse(strategies=strategy_status)


@app.post("/api/strategies/{name}/run", response_model=ActionResponse)
def run_strategy(name: str):
    if name not in strategy_status:
        raise StrategyNotFoundError(name)
    strategy_status[name] = "running"
    logger.info("strategy_started", strategy=name)
    return ActionResponse(status="running", strategy=name)


@app.post("/api/strategies/{name}/stop", response_model=ActionResponse)
def stop_strategy(name: str):
    if name not in strategy_status:
        raise StrategyNotFoundError(name)
    strategy_status[name] = "stopped"
    logger.info("strategy_stopped", strategy=name)
    return ActionResponse(status="stopped", strategy=name)


@app.get("/api/status", response_model=PlatformStatus)
def get_platform_status():
    return PlatformStatus(
        strategies=strategy_status,
        active_connections=len(manager.active_connections),
    )


@app.websocket("/ws/market_data")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            if not raw:
                continue

            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_text(f"ACK: {raw}")
                continue

            allowed = manager.check_rate_limit(websocket)
            if not allowed:
                await websocket.send_text(json.dumps({"error": "rate_limit_exceeded", "detail": "Too many messages"}))
                await websocket.close(code=1008)
                break

            await websocket.send_text(json.dumps({"type": "echo", "data": msg}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


async def _broadcast_market_state():
    while True:
        if manager.active_connections:
            await manager.broadcast({
                "type": "orderbook_update",
                "symbol": "BTC/USDT",
                "best_bid": 65000.0,
                "best_ask": 65001.0,
            })
        await asyncio.sleep(1.0)
