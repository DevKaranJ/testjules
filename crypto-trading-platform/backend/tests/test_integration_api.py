from fastapi.testclient import TestClient
from backend.api.main import app, manager
import pytest
import json

client = TestClient(app)


class TestHealth:
    def test_root_public(self):
        r = client.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_health_public(self):
        r = client.get("/api/health")
        assert r.status_code == 200
        assert r.json()["status"] in ("ok", "degraded")


class TestEndpoints:
    def test_backtests(self):
        r = client.get("/api/backtests")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_strategies(self):
        r = client.get("/api/strategies")
        assert r.status_code == 200
        assert "strategies" in r.json()

    def test_strategy_run_stop(self):
        r = client.post("/api/strategies/KalmanPairs/run")
        assert r.status_code == 200
        assert r.json()["status"] == "running"
        r = client.post("/api/strategies/KalmanPairs/stop")
        assert r.status_code == 200
        assert r.json()["status"] == "stopped"

    def test_strategy_not_found(self):
        r = client.post("/api/strategies/DoesNotExist/run")
        assert r.status_code == 404

    def test_platform_status(self):
        r = client.get("/api/status")
        assert r.status_code == 200
        assert "strategies" in r.json()
        assert "active_connections" in r.json()

    def test_backtest_detail_not_found(self):
        r = client.get("/api/backtests/99999")
        assert r.status_code == 404


class TestWebSocket:
    def test_plain_text_ping(self):
        with client.websocket_connect("/ws/market_data") as ws:
            ws.send_text("ping")
            data = ws.receive_text()
            assert data == "ACK: ping"

    def test_broadcast(self):
        with client.websocket_connect("/ws/market_data") as ws:
            import asyncio
            asyncio.run(manager.broadcast({"type": "test", "data": 1}))
            data = ws.receive_text()
            assert "test" in data
