from dishka import Provider, provide, Scope  # type: ignore
from ollama import Client

from lumen.config import Settings
from lumen.application.interfaces import LlmClient
from lumen.infrastructure.llms.ollama_client import OllamaLlmClient


class LlmProvider(Provider):
    @provide(scope=Scope.APP)
    def ollama_llm_client(self, settings: Settings) -> LlmClient:
        headers = {}
        if settings.ollama_token:
            headers["Authorization"] = f"Bearer {settings.ollama_token}"

        client = Client(host=settings.ollama_host, headers=headers)

        return OllamaLlmClient(client=client, model=settings.llm_model)
