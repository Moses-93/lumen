from typing import Callable, Any, NoReturn
import click

from lumen.application.dtos import Result, Failure, Success
from lumen.application.enums import AppError


def void(value: Any) -> None:
    """Explicitly ignores the value and returns None."""
    return None


def process_result[T, R](
    result: Result[T], on_success: Callable[[T], R], on_failure: Callable[[Failure], R]
) -> R:
    """Universal Result handler.

    Args:
        result: The Result object (Success or Failure).
        on_success: Function to be executed on success.
        on_failure: Function to be executed if an error occurs.

    Returns:
        The result of executing one of the functions (type R).
    """
    match result:
        case Success(data):
            return on_success(data)
        case Failure() as fail:
            return on_failure(fail)


def handle_failure(fail: Failure) -> NoReturn:
    """Maps a Failure object to a Click exception and raises it.

    Args:
        fail: The Failure object containing error details.

    Raises:
        click.ClickException: The mapped Click exception.
    """
    message = fail.message or "An unexpected error occurred."

    match fail.error:
        case AppError.VALIDATION_ERROR:
            raise click.BadParameter(message)
        case AppError.BAD_REQUEST | AppError.CONFLICT | AppError.UNPROCESSABLE_ENTITY:
            raise click.UsageError(message)
        case AppError.NOT_FOUND:
            raise click.ClickException(click.style(message, fg="yellow"))
        case AppError.UNAUTHORIZED | AppError.FORBIDDEN:
            raise click.ClickException(click.style(message, fg="red", bold=True))
        case _:
            raise click.ClickException(click.style(message, fg="red"))
