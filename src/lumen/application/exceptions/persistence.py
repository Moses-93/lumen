from .base import ApplicationError


class PersistenceError(ApplicationError):
    """Base exception for all persistent storage (database, cache, queues) related errors."""

    pass


class PersistenceConfigurationError(PersistenceError):
    """Raised when persistence layer configuration is invalid (e.g., missing driver, malformed URL)."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Persistence configuration error. Details: {details}")


class PersistenceConnectionError(PersistenceError):
    """Raised when a connection to the persistence layer cannot be established."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Connection to persistence layer failed. Details: {details}")


class PersistenceConstraintError(PersistenceError):
    """Raised when a data constraint is violated (e.g., unique, foreign key)."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Data constraint violated. Details: {details}")


class PersistenceInvalidDataError(PersistenceError):
    """Raised when invalid data is provided (wrong type, size, or format)."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Invalid data encountered. Details: {details}")


class PersistenceOperationalError(PersistenceError):
    """Raised when an operational error occurs (e.g., deadlock, locked resource)."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Operational error in persistence layer. Details: {details}")


class PersistenceQueryError(PersistenceError):
    """Raised when there is an error in the query syntax or structure."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Query/Execution error. Details: {details}")


class PersistenceAuthError(PersistenceError):
    """Raised when authentication with the persistence layer fails."""

    def __init__(self, details: str) -> None:
        super().__init__(
            f"Authentication with the persistence layer failed. Details: {details}"
        )


class PersistenceReplyError(PersistenceError):
    """Raised when the persistence server returns an error response."""

    def __init__(self, details: str) -> None:
        super().__init__(
            f"Persistence server returned an error response. Details: {details}"
        )


class PersistenceTimeoutError(PersistenceError):
    """Raised when an operation in the persistence layer times out."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Persistence layer operation timed out. Details: {details}")
