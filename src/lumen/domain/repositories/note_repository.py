from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from lumen.domain.entities import Note


class NoteRepository(ABC):
    @abstractmethod
    def add(self, note: Note, embedding: list[float]) -> Note:
        pass

    @abstractmethod
    def get_by_id(self, note_id: UUID) -> Note | None:
        pass

    @abstractmethod
    def get_all(
        self,
        limit: int = 10,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Note]:
        pass

    @abstractmethod
    def find_similar(
        self,
        embedding: list[float],
        limit: int = 5,
        threshold: float = 0.28,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Note]:
        pass

    @abstractmethod
    def delete(self, note_id: UUID) -> None:
        pass
