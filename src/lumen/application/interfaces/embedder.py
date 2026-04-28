from typing import Protocol, Iterable


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...

    def embed_many(
        self, texts: Iterable[str], batch_size: int = 256
    ) -> Iterable[list[float]]: ...
