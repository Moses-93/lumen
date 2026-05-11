from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(slots=True, frozen=True)
class Note:
    """Represents a single note entity.

    Attributes:
        text: The content of the note.
        moods: A list of moods associated with the note.
        created_at: The timestamp when the note was created.
        id: The unique identifier of the note.
    """

    text: str
    moods: list[str] = field(default_factory=list[str])
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=uuid4)
