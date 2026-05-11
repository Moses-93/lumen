from types import TracebackType
from typing import Protocol, Self

from lumen.domain.repositories import NoteRepository, QuoteRepository


class Session(Protocol):
    """Provides a gateway for managing the lifecycle of persistence operations."""

    def commit(self) -> None:
        """Persists all staged changes to the underlying storage.

        Raises:
            PersistenceError: If the commit operation fails.
        """
        ...

    def rollback(self) -> None:
        """Reverts all staged changes in the current session.

        Raises:
            PersistenceError: If the rollback operation fails.
        """
        ...

    def close(self) -> None:
        """Closes the session and releases associated resources.

        Raises:
            PersistenceError: If the close operation fails.
        """
        ...


class Transaction(Protocol):
    """Represents an atomic boundary for persistence operations."""

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
        /,
    ) -> None:
        """Finalizes the transaction.

        If an exception was raised within the context, the transaction is rolled back.
        Otherwise, staged changes are committed to the storage.

        Raises:
            PersistenceError: If the commit or rollback operation fails.
        """
        ...


class UnitOfWork(Protocol):
    """Coordinates repositories and underlying persistence sessions."""

    @property
    def notes(self) -> NoteRepository:
        """Provides access to the note repository."""
        ...

    @property
    def quotes(self) -> QuoteRepository:
        """Provides access to the quote repository."""
        ...

    def transaction(self) -> Transaction:
        """Provides an atomic boundary for persistence operations.

        Returns:
            A transaction context manager.
        """
        ...

    def save(self) -> None:
        """Persists all modifications made during the current work scope.

        Must be called inside a transaction context. Calling outside of it
        is a silent no-op.

        Example:
            with uow.transaction():
                uow.quotes.save(quote, embedding)
                uow.save()
        """
        ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Finalizes the unit of work and releases underlying resources."""
        ...
