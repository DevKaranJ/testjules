from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import init_db

# Use SQLite by default for easy running without external dependencies.
# Can be replaced with postgresql://user:password@localhost/dbname
DATABASE_URL = "sqlite:///crypto_trading.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():
    init_db(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
