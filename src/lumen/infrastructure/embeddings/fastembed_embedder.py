from fastembed import TextEmbedding
from typing import Iterable
from pathlib import Path
import warnings


class FastembedEmbedder:
    def __init__(
        self, model: str, prefix: str, cuda: bool, cache_dir: Path | None = None
    ) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            self._model = TextEmbedding(
                model_name=model,
                cache_dir=str(cache_dir) if cache_dir else None,
                cuda=cuda,
            )
        self._prefix = prefix

    def embed(self, text: str) -> list[float]:
        return next(
            iter(self._model.embed(f"{self._prefix.removesuffix(':')}: {text}"))
        ).tolist()

    def embed_many(
        self, texts: Iterable[str], batch_size: int = 256
    ) -> Iterable[list[float]]:
        prefixed_texts = (f"{self._prefix.removesuffix(':')}: {text}" for text in texts)
        for e in self._model.embed(prefixed_texts, batch_size=batch_size):
            yield e.tolist()
