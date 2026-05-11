from enum import StrEnum, auto


class AppError(StrEnum):
    """Enumeration of application-level error types for Result objects."""

    NOT_FOUND = auto()
    CONFLICT = auto()
    VALIDATION_ERROR = auto()
    UNAUTHORIZED = auto()
    FORBIDDEN = auto()
    INTERNAL_ERROR = auto()
    BAD_REQUEST = auto()
    UNPROCESSABLE_ENTITY = auto()
    TOO_MANY_REQUESTS = auto()
    SERVICE_UNAVAILABLE = auto()
