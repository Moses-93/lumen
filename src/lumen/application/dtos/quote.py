from pydantic import BaseModel, Field

from lumen.domain.entities import Quote


class SeedQuoteCommand(BaseModel):
    """Command DTO for seeding a single quote."""

    author: str
    domain: str | None = None
    text: str
    semantic_tags: list[str] = Field(default_factory=list)

    def to_entity(self) -> Quote:
        return Quote(
            author=self.author,
            domain=self.domain,
            text=self.text,
            tags=self.semantic_tags,
        )
