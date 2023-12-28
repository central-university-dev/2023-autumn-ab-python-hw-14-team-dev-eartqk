from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    'postgresql://postgres:postgres@postgres:5432/homework_db',  # TODO: get env there
    # echo=True,
)


Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Session:
    """Dependency for getting session"""
    session = Session()
    try:
        yield session
    finally:
        session.close()
