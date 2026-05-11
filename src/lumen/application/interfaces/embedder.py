from collections.abc import Iterable
from typing import Protocol


class Embedder(Protocol):
    """Interface for text embedding generation.

    Provides methods to convert textual input into vector representations
    suitable for semantic similarity operations.
    """

    def embed(self, text: str) -> list[float]:
        """Generates a vector embedding for a single text string.

        Args:
            text: The input string to be embedded.

        Returns:
            A list of floating-point values representing the text embedding.

        Raises:
            EmbeddingError: If the text cannot be embedded.
        """
        ...

    def embed_many(
        self, texts: Iterable[str], batch_size: int = 256
    ) -> Iterable[list[float]]:
        """Generates vector embeddings for multiple text strings.

        Args:
            texts: An iterable of strings to be embedded.
            batch_size: The number of texts to process in a single batch.

        Returns:
            An iterable of vector embeddings.

        Raises:
            EmbeddingError: If the texts cannot be embedded.
        """
        ...
