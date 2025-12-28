from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

from config import get_settings

settings = get_settings()
database_url = settings.database_url
url = make_url(database_url)

connect_args = {}
if url.drivername.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
