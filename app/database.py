"""Database engine, session factory, and base model setup."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# pool_pre_ping ensures stale connections are detected and recycled
engine = create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session and close it once its done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
