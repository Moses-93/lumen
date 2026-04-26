from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import (
    ProgrammingError,
    OperationalError,
    ArgumentError,
    NoSuchModuleError,
)

from lumen.application.exceptions.persistence import (
    PersistenceConfigurationError,
    PersistenceOperationalError,
)


def init_engine(url: str) -> Engine:
    try:
        return create_engine(
            url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=5,
            max_overflow=10,
        )
    except (ArgumentError, NoSuchModuleError) as error:
        raise PersistenceConfigurationError(str(error)) from error


def init_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)


def enable_pgvector(engine: Engine) -> None:
    """Enable pgvector extension on the database."""
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    except (ProgrammingError, OperationalError) as error:
        raise PersistenceOperationalError(
            "Failed to enable pgvector extension. Ensure 'pgvector' is installed on the PostgreSQL server and the user has sufficient privileges."
        ) from error
