from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone


@dataclass(slots=True, frozen=True)
class Note:
    text: str
    moods: list[str] = field(default_factory=list[str])
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: UUID = field(default_factory=uuid4)
