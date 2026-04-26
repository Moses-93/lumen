from dataclasses import dataclass

from lumen.application.enums import AppError


@dataclass(frozen=True, slots=True)
class Success[T]:
    data: T


@dataclass(frozen=True, slots=True)
class Failure:
    error: str | AppError
    message: str


type Result[T] = Success[T] | Failure
