from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import init_db

import os

# Use environment variable for Postgres in Docker, fallback to SQLite for local dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crypto_trading.db")

# check_same_thread is only valid for sqlite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():
    init_db(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
