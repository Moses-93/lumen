from typing import Any
from .base import DomainError


class QuoteError(DomainError):
    """The base exception for quote-related errors."""

    pass


class QuoteAuthorInvalidError(QuoteError):
    """Raised when the author name does not meet requirements."""

    def __init__(self, name: Any) -> None:
        self.name = name
        super().__init__(f"Author name '{name}' is invalid. Must be 3-255 characters.")


class QuoteTextInvalidError(QuoteError):
    """Raised when the quote text is invalid (empty or too long)."""

    def __init__(self, text: str) -> None:
        self.text = text
        super().__init__(f"Invalid quote text: {text}")


class QuoteNotFoundError(QuoteError):
    """Raised when a quote cannot be found."""

    def __init__(self, quote_id: Any) -> None:
        self.quote_id = quote_id
        super().__init__(f"Quote with ID '{quote_id}' not found.")
