from typing import Protocol, Self
from types import TracebackType

from lumen.domain.repositories import QuoteRepository, NoteRepository


class Session(Protocol):
    """
    Provides a gateway for managing the lifecycle of persistence operations.
    """

    def commit(self) -> None:
        """
        Persists all staged changes to the underlying storage.

        :raises PersistenceError: If the commit operation fails.
        """
        ...

    def rollback(self) -> None:
        """
        Reverts all staged changes in the current session.

        :raises PersistenceError: If the rollback operation fails.
        """
        ...

    def close(self) -> None:
        """
        Closes the session and releases associated resources.

        :raises PersistenceError: If the close operation fails.
        """
        ...


class Transaction(Protocol):
    """
    Represents an atomic boundary for persistence operations.
    """

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
        /,
    ) -> None:
        """
        Finalize the transaction.

        If an exception was raised within the context, the transaction is rolled back.
        Otherwise, staged changes are committed to the storage.

        :raises PersistenceError: If the commit or rollback operation fails.
        """
        ...


class UnitOfWork(Protocol):
    """
    Orchestrates the lifecycle of repositories and underlying persistence sessions.
    """

    @property
    def notes(self) -> NoteRepository: ...

    @property
    def quotes(self) -> QuoteRepository: ...

    def transaction(self) -> Transaction:
        """
        Provides an atomic boundary for persistence operations.
        """
        ...

    def save(self) -> None:
        """Persists all modifications made during the current work scope.

        Must be called inside a :meth:`transaction` context.
        Calling outside of it is a silent no-op — changes will be lost.

        Example::

            with uow.transaction():
                uow.quotes.save(quote)
                uow.save()  # commits all changes atomically
        """
        ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Finalizes the unit of work and releases underlying resources.
        """
        ...
