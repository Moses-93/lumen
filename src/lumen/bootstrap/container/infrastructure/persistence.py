from typing import Iterable

from dishka import Provider, Scope, provide  # type: ignore
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from lumen.config import Settings
from lumen.domain.repositories import (
    QuoteRepository,
    NoteRepository,
)
from lumen.infrastructure.persistence.postgres.repositories import (
    PostgresNoteRepository,
    PostgresQuoteRepository,
)
from lumen.application.interfaces.unit_of_work import UnitOfWork
from lumen.infrastructure.persistence.postgres.unit_of_work import PostgresUnitOfWork
from lumen.infrastructure.persistence.postgres.config import (
    init_engine,
    enable_pgvector,
    init_sessionmaker,
)


class PostgresProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self, settings: Settings) -> Iterable[Engine]:
        engine = init_engine(settings.postgres_url())
        enable_pgvector(engine)
        yield engine
        engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: Engine) -> sessionmaker[Session]:
        return init_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    def session(self, session_factory: sessionmaker[Session]) -> Iterable[Session]:
        with session_factory() as session:
            yield session


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def note_repository(self, session: Session) -> NoteRepository:
        return PostgresNoteRepository(session)

    @provide(scope=Scope.REQUEST)
    def quote_repository(self, session: Session) -> QuoteRepository:
        return PostgresQuoteRepository(session)

    @provide(scope=Scope.REQUEST)
    def unit_of_work(self, session: Session) -> Iterable[UnitOfWork]:
        with PostgresUnitOfWork(session) as uow:
            yield uow
