from pydantic import BaseModel, Field

from lumen.domain.entities import Quote


class SeedQuoteCommand(BaseModel):
    """Command DTO for seeding a single quote."""

    author: str
    domain: str | None = None
    text: str
    source: str | None = None
    tags: list[str] = Field(default_factory=list)

    def to_entity(self) -> Quote:
        """Converts command data to a Quote domain entity.

        Returns:
            A new Quote entity instance.
        """
        return Quote.new(
            author=self.author,
            domain=self.domain,
            source=self.source,
            text=self.text,
            tags=self.tags,
        )
