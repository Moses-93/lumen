from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from lumen.domain.entities import Note


class NoteRepository(ABC):
    """Interface for Note entity persistence.

    Defines the contract for storing, retrieving, and searching notes.
    """

    @abstractmethod
    def add(self, note: Note, embedding: list[float]) -> Note:
        """Persists a new note along with its vector embedding.

        Args:
            note: The note entity to be persisted.
            embedding: The vector representation of the note content.

        Returns:
            The persisted note entity with its assigned identity.

        Raises:
            PersistenceError: If the note cannot be persisted.
        """
        pass

    @abstractmethod
    def get_by_id(self, note_id: UUID) -> Note | None:
        """Retrieves a note by its unique identifier.

        Args:
            note_id: The UUID of the note to retrieve.

        Returns:
            The note entity if found, otherwise None.

        Raises:
            PersistenceError: If the note cannot be retrieved.
        """
        pass

    @abstractmethod
    def get_all(
        self,
        limit: int = 10,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Note]:
        """Retrieves a paginated list of notes with optional temporal filtering.

        Args:
            limit: Maximum number of notes to return.
            offset: Number of notes to skip for pagination.
            from_date: Inclusive start date for filtering.
            to_date: Inclusive end date for filtering.

        Returns:
            A list of note entities matching the criteria.

        Raises:
            PersistenceError: If the notes cannot be retrieved.
        """
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
        """Searches for notes with semantic similarity to the provided embedding.

        Args:
            embedding: The query vector to compare against.
            limit: Maximum number of similar notes to return.
            threshold: Minimum similarity score required for results.
            from_date: Inclusive start date for filtering.
            to_date: Inclusive end date for filtering.

        Returns:
            A list of notes ordered by similarity to the query vector.

        Raises:
            PersistenceError: If the notes cannot be retrieved.
        """
        pass

    @abstractmethod
    def delete(self, note_id: UUID) -> None:
        """Removes a note from persistence.

        Args:
            note_id: The unique identifier of the note to delete.

        Raises:
            PersistenceError: If the note cannot be deleted.
        """
        pass
