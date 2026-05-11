from dataclasses import dataclass

from lumen.domain.exceptions import QuoteAuthorInvalidError


@dataclass(slots=True, frozen=True)
class Author:
    """Represents the author of the quote.

    Attributes:
        value: The validated author name.

    Raises:
        QuoteAuthorInvalidError: If the author name is invalid.
    """

    value: str

    def __post_init__(self) -> None:
        cleaned_value = self.value.strip()

        if not (2 <= len(cleaned_value) <= 255):
            raise QuoteAuthorInvalidError(cleaned_value)

        if cleaned_value.islower() or cleaned_value.isupper():
            cleaned_value = cleaned_value.title()

        object.__setattr__(self, "value", cleaned_value)

    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)
