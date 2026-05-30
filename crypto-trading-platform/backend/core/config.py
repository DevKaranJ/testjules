from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # Database
    database_url: str = "sqlite:///crypto_trading.db"

    # Exchange
    exchange_id: str = "binance"
    api_key: str = ""
    api_secret: str = ""
    testnet: bool = True

    # Risk defaults
    starting_equity: float = 100000.0
    max_risk_pct: float = 0.01
    max_consecutive_losses: int = 3
    max_daily_drawdown_pct: float = 0.05

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


settings = Settings()
