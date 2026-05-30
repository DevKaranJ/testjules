from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .models import init_db
from ..core.config import settings
from structlog import get_logger

logger = get_logger()

connect_args = {"check_same_thread": False} if settings.is_sqlite else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_database():
    init_db(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("db_connection_failed", error=str(e))
        return False
