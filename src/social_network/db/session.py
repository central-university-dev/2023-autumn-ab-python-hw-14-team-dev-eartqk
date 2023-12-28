from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.social_network.settings import settings

engine = create_engine(settings.database_url)


SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Generator[Session, None, None]:
    """Dependency for getting session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
