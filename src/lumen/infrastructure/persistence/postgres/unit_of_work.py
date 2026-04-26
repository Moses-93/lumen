from typing import Any, Self
from sqlalchemy.orm import Session

from lumen.application.interfaces import Transaction
from lumen.infrastructure.persistence.postgres.repositories import (
    PostgresNoteRepository,
    PostgresQuoteRepository,
)


class PostgresUnitOfWork:
    def __init__(self, session: Session):
        self.session = session
        self._repositories: dict[type, object] = {}

    def transaction(self) -> Transaction:
        if self.session.in_transaction():
            return self.session.begin_nested()
        return self.session.begin()

    def save(self) -> None:
        if self.session.in_transaction():
            self.session.commit()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._repositories.clear()

    def _get_repository[T](self, repository_type: type[T]) -> T:
        if repository_type not in self._repositories:
            self._repositories[repository_type] = repository_type(self.session)  # type: ignore
        return self._repositories[repository_type]  # type: ignore

    @property
    def notes(self) -> PostgresNoteRepository:
        return self._get_repository(PostgresNoteRepository)

    @property
    def quotes(self) -> PostgresQuoteRepository:
        return self._get_repository(PostgresQuoteRepository)
