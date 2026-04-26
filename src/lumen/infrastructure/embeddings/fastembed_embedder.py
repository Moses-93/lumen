from fastembed import TextEmbedding
from pathlib import Path
import warnings


class FastembedEmbedder:
    def __init__(self, model: str, prefix: str, cache_dir: Path | None = None) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            self._model = TextEmbedding(
                model, cache_dir=str(cache_dir) if cache_dir else None
            )
        self._prefix = prefix

    def embed(self, text: str) -> list[float]:
        return next(
            iter(self._model.embed(f"{self._prefix.removesuffix(':')}: {text}"))
        ).tolist()
