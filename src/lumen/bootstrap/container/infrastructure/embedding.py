from dishka import Provider, provide, Scope, FromComponent  # type: ignore[attr-defined]

from typing import Literal, Annotated

from lumen.application.interfaces import Embedder
from lumen.infrastructure.embeddings import FastembedEmbedder
from lumen.config import Settings


class EmbedderProvider(Provider):
    scope = Scope.APP

    def __init__(self, component: Literal["query", "passage"]) -> None:
        super().__init__(component=component)
        self.prefix = component

    @provide()
    def embedder(self, settings: Annotated[Settings, FromComponent("")]) -> Embedder:
        return FastembedEmbedder(
            model=settings.embedding_model,
            prefix=self.prefix,
            cuda=settings.use_gpu,
            cache_dir=settings.embedding_cache_dir,
        )
