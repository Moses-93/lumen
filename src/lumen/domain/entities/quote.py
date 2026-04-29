from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from lumen.domain.value_objects import Author, QuoteText


@dataclass(slots=True)
class Quote:
    author: Author
    text: QuoteText
    domain: str | None
    source: str | None
    tags: list[str] = field(default_factory=list[str])
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: UUID = field(default_factory=uuid4)

    @classmethod
    def new(
        cls,
        author: str,
        text: str,
        tags: list[str] | None = None,
        domain: str | None = None,
        source: str | None = None,
    ) -> Quote:
        """Factory method to create a new Quote from primitives.

        Raises:
            QuoteAuthorInvalidError: If the author name is invalid.
            QuoteTextInvalidError: If the quote text is invalid.
        """
        return cls(
            author=Author(author),
            text=QuoteText(text),
            tags=tags or [],
            domain=domain,
            source=source,
        )

    @classmethod
    def reconstruct(
        cls,
        id: UUID,
        author: str,
        text: str,
        created_at: datetime,
        updated_at: datetime,
        tags: list[str],
        domain: str | None = None,
        source: str | None = None,
    ) -> Quote:
        """Reconstructs a Quote from raw data.

        Raises:
            QuoteAuthorInvalidError: If the author name is invalid.
            QuoteTextInvalidError: If the quote text is invalid.
        """
        return cls(
            id=id,
            author=Author(author),
            text=QuoteText(text),
            tags=tags,
            domain=domain,
            source=source,
            created_at=created_at,
            updated_at=updated_at,
        )
