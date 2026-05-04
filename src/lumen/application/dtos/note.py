from datetime import datetime

from pydantic import BaseModel, Field

from lumen.domain.entities import Note


class AddNoteCommand(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    moods: list[str] = Field(default_factory=list)

    def to_entity(self) -> Note:
        return Note(
            text=self.text,
            moods=self.moods,
        )


class GetNotesQuery(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    from_date: datetime | None = Field(default=None)
    to_date: datetime | None = Field(default=None)


class FindSimilarNotesQuery(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    limit: int = Field(default=5, ge=1, le=100)
    threshold: float = Field(default=0.28, ge=0.0, le=1.0)
    from_date: datetime | None = Field(default=None)
    to_date: datetime | None = Field(default=None)
