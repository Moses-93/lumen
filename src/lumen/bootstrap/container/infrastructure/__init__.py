from dishka import Provider

from .embedding import EmbedderProvider
from .llm import LlmProvider
from .persistence import PostgresProvider, RepositoryProvider


def infrastructure_providers() -> list[Provider]:
    return [
        PostgresProvider(),
        RepositoryProvider(),
        EmbedderProvider(component="query"),
        EmbedderProvider(component="passage"),
        LlmProvider(),
    ]
