from dataclasses import dataclass

from lumen.application.enums import AppError


@dataclass(frozen=True, slots=True)
class Success[T]:
    """Result object representing a successful operation."""

    data: T

    def __bool__(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class Failure:
    """Result object representing a failed operation."""

    error: str | AppError
    message: str

    def __bool__(self) -> bool:
        return False


type Result[T] = Success[T] | Failure
