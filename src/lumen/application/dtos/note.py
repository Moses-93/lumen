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
