from ollama import Client, ResponseError

from lumen.application.exceptions import (
    LlmConnectionError,
    LlmResponseError,
    LlmModelNotFoundError,
    LlmAuthenticationError,
)


class OllamaLlmClient:
    def __init__(self, client: Client, model: str) -> None:
        self._client = client
        self._model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self._client.generate(
                model=self._model,
                prompt=prompt,
            )
            return response.response
        except ResponseError as e:
            if e.status_code == 404:
                raise LlmModelNotFoundError(model_name=self._model) from e
            if e.status_code in (401, 403):
                raise LlmAuthenticationError(details=str(e)) from e
            raise LlmResponseError(response=str(e)) from e
        except ConnectionError as e:
            raise LlmConnectionError(details=str(e)) from e
