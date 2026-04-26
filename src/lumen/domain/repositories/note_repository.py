from abc import ABC, abstractmethod
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
    def get_all(self, limit: int = 10, offset: int = 0) -> list[Note]:
        pass

    @abstractmethod
    def delete(self, note_id: UUID) -> None:
        pass
