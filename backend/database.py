from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import get_database_settings

Base = declarative_base()


def _build_engine(database_url: str) -> Engine:
    url = make_url(database_url)
    connect_args = {}
    if url.drivername.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    return create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)


@lru_cache()
def get_engine() -> Engine:
    settings = get_database_settings()
    return _build_engine(settings.database_url)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
