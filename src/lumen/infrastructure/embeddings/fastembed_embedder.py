import warnings
from collections.abc import Iterable
from pathlib import Path

from fastembed import TextEmbedding

from lumen.application.exceptions import (
    EmbeddingInferenceError,
    EmbeddingInitializationError,
)


class FastembedEmbedder:
    def __init__(
        self, model: str, prefix: str, cuda: bool, cache_dir: Path | None = None
    ) -> None:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                self._model = TextEmbedding(
                    model_name=model,
                    cache_dir=str(cache_dir) if cache_dir else None,
                    cuda=cuda,
                )
        except (ValueError, RuntimeError) as e:
            raise EmbeddingInitializationError(model_name=model, details=str(e)) from e
        self._prefix = prefix

    def embed(self, text: str) -> list[float]:
        try:
            return next(
                iter(self._model.embed(f"{self._prefix.removesuffix(':')}: {text}"))
            ).tolist()
        except (ValueError, RuntimeError) as e:
            raise EmbeddingInferenceError(str(e)) from e

    def embed_many(
        self, texts: Iterable[str], batch_size: int = 256
    ) -> Iterable[list[float]]:
        prefixed_texts = (f"{self._prefix.removesuffix(':')}: {text}" for text in texts)
        try:
            for e in self._model.embed(prefixed_texts, batch_size=batch_size):
                yield e.tolist()
        except (ValueError, RuntimeError) as e:
            raise EmbeddingInferenceError(str(e)) from e
