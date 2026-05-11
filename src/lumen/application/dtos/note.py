from datetime import datetime

from pydantic import BaseModel, Field

from lumen.domain.entities import Note


class AddNoteCommand(BaseModel):
    """Command for creating a new note entity."""

    text: str = Field(..., min_length=1, max_length=5000)
    moods: list[str] = Field(default_factory=list)

    def to_entity(self) -> Note:
        """Converts command data to a Note domain entity.

        Returns:
            A new Note entity instance.
        """
        return Note(
            text=self.text,
            moods=self.moods,
        )


class GetNotesQuery(BaseModel):
    """Parameters for retrieving a filtered list of notes."""

    limit: int = Field(default=10, ge=1, le=100)
    from_date: datetime | None = Field(default=None)
    to_date: datetime | None = Field(default=None)


class FindSimilarNotesQuery(BaseModel):
    """Parameters for semantic search across existing notes."""

    text: str = Field(..., min_length=1, max_length=5000)
    limit: int = Field(default=5, ge=1, le=100)
    threshold: float = Field(default=0.28, ge=0.0, le=1.0)
    from_date: datetime | None = Field(default=None)
    to_date: datetime | None = Field(default=None)
