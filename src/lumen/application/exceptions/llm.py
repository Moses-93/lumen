from .base import ApplicationError


class LlmError(ApplicationError):
    """Base exception for all Large Language Model related errors."""

    pass


class LlmConfigurationError(LlmError):
    """Raised when LLM configuration is invalid."""

    def __init__(self, details: str) -> None:
        super().__init__(f"LLM configuration error. Details: {details}")


class LlmConnectionError(LlmError):
    """Raised when a connection to the LLM provider cannot be established."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Connection to LLM provider failed. Details: {details}")


class LlmAuthenticationError(LlmError):
    """Raised when authentication with the LLM provider fails."""

    def __init__(self, details: str | None = None) -> None:
        message = "Authentication with the LLM provider failed."
        if details:
            message += f" Details: {details}"
        super().__init__(message)


class LlmResponseError(LlmError):
    """Raised when the LLM returns an error response or malformed data."""

    def __init__(self, response: str) -> None:
        super().__init__(f"LLM provider returned invalid response: {response}")


class LlmTimeoutError(LlmError):
    """Raised when an operation with the LLM provider times out."""

    def __init__(self) -> None:
        super().__init__("LLM operation timed out.")


class LlmTokenLimitError(LlmError):
    """Raised when the request exceeds the model's token limit."""

    def __init__(self, limit: int, actual: int | None = None) -> None:
        message = f"LLM token limit exceeded (Limit: {limit})"
        if actual:
            message += f", Actual: {actual}"
        super().__init__(message)


class LlmOperationalError(LlmError):
    """Raised when an operational error occurs during LLM inference."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Operational error in LLM layer. Details: {details}")


class LlmModelNotFoundError(LlmError):
    """Raised when the requested model is not found on the provider's server."""

    def __init__(self, model_name: str) -> None:
        super().__init__(
            f"Model '{model_name}' not found. You might need to pull it first."
        )
