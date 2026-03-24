from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Use SQLite only for local development; PostgreSQL for all other environments
db_url = settings.DATABASE_URL
if settings.APP_ENV == "development" and "postgresql" in db_url:
    db_url = "sqlite:///./eduequity.db"

connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}
engine = create_engine(db_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
