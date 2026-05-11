from abc import ABC, abstractmethod
from uuid import UUID

from lumen.domain.entities import Quote


class QuoteRepository(ABC):
    """Interface for Quote entity persistence.

    Defines the contract for managing philosophical quotes.
    """

    @abstractmethod
    def save(self, quote: Quote, embedding: list[float]) -> Quote:
        """Persists a quote and its associated vector embedding.

        Args:
            quote: The quote entity to be saved.
            embedding: The vector representation of the quote content.

        Returns:
            The saved quote entity.

        Raises:
            PersistenceError: If the quote cannot be persisted.
        """
        pass

    @abstractmethod
    def save_many(self, quotes: list[tuple[Quote, list[float]]]) -> list[Quote]:
        """Persists multiple quotes with their respective embeddings.

        Args:
            quotes: A list of tuples containing a quote and its embedding.

        Returns:
            A list of successfully persisted quote entities.

        Raises:
            PersistenceError: If the quotes cannot be persisted.
        """
        pass

    @abstractmethod
    def get_all(self) -> list[Quote]:
        """Retrieves all persisted quotes.

        Returns:
            A list containing all quote entities in the storage.

        Raises:
            PersistenceError: If the quotes cannot be retrieved.
        """
        pass

    @abstractmethod
    def get_by_id(self, quote_id: UUID) -> Quote | None:
        """Retrieves a quote by its unique identifier.

        Args:
            quote_id: The UUID of the quote to retrieve.

        Returns:
            The quote entity if found, otherwise None.

        Raises:
            PersistenceError: If the quote cannot be retrieved.
        """
        pass

    @abstractmethod
    def delete(self, quote_id: UUID) -> None:
        """Removes a quote from persistence.

        Args:
            quote_id: The unique identifier of the quote to delete.

        Raises:
            PersistenceError: If the quote cannot be deleted.
        """
        pass

    @abstractmethod
    def find_similar(
        self, embedding: list[float], limit: int = 1, threshold: float = 0.28
    ) -> list[Quote]:
        """Searches for quotes semantically similar to the provided embedding.

        Args:
            embedding: The query vector to compare against.
            limit: Maximum number of similar quotes to return.
            threshold: Minimum similarity score required for results.

        Returns:
            A list of quotes ordered by similarity to the query vector.

        Raises:
            PersistenceError: If the quotes cannot be retrieved.
        """
        pass
