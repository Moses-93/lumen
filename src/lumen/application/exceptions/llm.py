from .base import ApplicationError


class LlmError(ApplicationError):
    """Base exception for all Large Language Model related errors."""

    pass


class LlmConfigurationError(LlmError):
    """Raised when LLM configuration is invalid (e.g., missing model name, invalid parameters)."""

    def __init__(self, details: str) -> None:
        super().__init__(f"LLM configuration error. Details: {details}")


class LlmConnectionError(LlmError):
    """Raised when a connection to the LLM provider (API or local server) cannot be established."""

    def __init__(self, details: str) -> None:
        super().__init__(f"Connection to LLM provider failed. Details: {details}")


class LlmAuthenticationError(LlmError):
    """Raised when authentication with the LLM provider fails (e.g., invalid API key)."""

    def __init__(self, details: str | None = None) -> None:
        """
        :param details: Optional authentication failure details.
        """
        message = "Authentication with the LLM provider failed."
        if details:
            message += f" Details: {details}"
        super().__init__(message)


class LlmResponseError(LlmError):
    """Raised when the LLM returns an error response or malformed data."""

    def __init__(self, response: str) -> None:
        """
        :param response: The raw response or error message from the provider.
        """
        super().__init__(f"LLM provider returned invalid response: {response}")


class LlmTimeoutError(LlmError):
    """Raised when an operation with the LLM provider times out."""

    def __init__(self) -> None:
        super().__init__("LLM operation timed out.")


class LlmTokenLimitError(LlmError):
    """Raised when the request exceeds the model's token limit or context window."""

    def __init__(self, limit: int, actual: int | None = None) -> None:
        """
        :param limit: The maximum token limit allowed.
        :param actual: Optional actual number of tokens used.
        """
        message = f"LLM token limit exceeded (Limit: {limit})"
        if actual:
            message += f", Actual: {actual}"
        super().__init__(message)


class LlmOperationalError(LlmError):
    """Raised when an operational error occurs during LLM inference."""

    def __init__(self, details: str) -> None:
        """
        :param details: Details of the operational failure.
        """
        super().__init__(f"Operational error in LLM layer. Details: {details}")


class LlmModelNotFoundError(LlmError):
    """Raised when the requested model is not found on the provider's server/host."""

    def __init__(self, model_name: str) -> None:
        """
        :param model_name: Name of the missing model.
        """
        super().__init__(
            f"Model '{model_name}' not found. You might need to pull it first."
        )
