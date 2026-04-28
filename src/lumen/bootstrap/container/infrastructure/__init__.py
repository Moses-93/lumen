from dishka import Provider

from .embedding import EmbedderProvider
from .persistence import PostgresProvider, RepositoryProvider
from .llm import LlmProvider


def infrastructure_providers() -> list[Provider]:
    return [
        PostgresProvider(),
        RepositoryProvider(),
        EmbedderProvider(component="query"),
        EmbedderProvider(component="passage"),
        LlmProvider(),
    ]
