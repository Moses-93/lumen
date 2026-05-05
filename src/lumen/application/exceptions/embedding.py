from .base import ApplicationError


class EmbeddingError(ApplicationError):
    """Base exception for all embedding-related errors."""

    pass


class EmbeddingInitializationError(EmbeddingError):
    """Raised when the embedding model fails to initialize."""

    def __init__(self, model_name: str, details: str) -> None:
        super().__init__(
            f"Failed to initialize embedding model: {model_name}. Details: {details}"
        )


class EmbeddingInferenceError(EmbeddingError):
    """Raised when an error occurs during the embedding inference process."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Embedding inference failed. Details: {details}")
