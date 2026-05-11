from dataclasses import dataclass

from lumen.domain.exceptions import QuoteTextInvalidError


@dataclass(slots=True, frozen=True)
class QuoteText:
    """Represents the validated text content of a quote.

    Attributes:
        value: The validated quote text.

    Raises:
        QuoteTextInvalidError: If the text length is outside [10, 2000].
    """

    value: str

    def __post_init__(self) -> None:
        cleaned_value = self.value.strip()

        if not (10 <= len(cleaned_value) <= 2000):
            raise QuoteTextInvalidError(cleaned_value)

        object.__setattr__(self, "value", cleaned_value)

    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)
