from itertools import batched
from typing import Iterable

from lumen.application.dtos import Success, Failure, Result, SeedQuoteCommand
from lumen.application.interfaces import Embedder, UnitOfWork
from lumen.application.enums import AppError
from lumen.domain.entities import Quote


class SeedQuotesInteractor:
    """Handles bulk seeding of quotes."""

    def __init__(
        self,
        embedder: Embedder,
        uow: UnitOfWork,
    ) -> None:
        self._embedder = embedder
        self._uow = uow

    def execute(
        self, commands: Iterable[SeedQuoteCommand], batch_size: int = 64
    ) -> Iterable[Result[int]]:
        """Seeds quotes in batches.

        Args:
            commands: Collection of seeding commands.
            batch_size: Processing batch size.

        Yields:
            Progress results with total count of seeded quotes.
        """
        total_count = 0
        for chunk in batched(commands, batch_size):
            quotes = [cmd.to_entity() for cmd in chunk]
            embeddings = self._embedder.embed_many(
                (self._build_embedding_text(q) for q in quotes),
                batch_size=batch_size,
            )

            with self._uow.transaction():
                if not self._uow.quotes.save_many(list(zip(quotes, embeddings))):
                    return Failure(AppError.INTERNAL_ERROR, "Failed to save batch")
                self._uow.save()

            total_count += len(quotes)
            yield Success(total_count)

    def _build_embedding_text(self, quote: Quote) -> str:
        parts = [str(quote.text)]
        if quote.domain:
            parts.append(quote.domain)
        if quote.tags:
            parts.extend(quote.tags)
        return " ".join(parts)


class FindQuotesInteractor:
    """Orchestrates semantic search for quotes based on query similarity."""

    def __init__(self, embedder: Embedder, uow: UnitOfWork) -> None:
        self._embedder = embedder
        self._uow = uow

    def execute(
        self, query: str, limit: int = 1, threshold: float = 0.28
    ) -> Result[list[Quote]]:
        """Finds quotes semantically resonant with the provided query.

        Args:
            query: Semantic search query string.
            limit: Maximum number of quotes to retrieve.
            threshold: Minimum similarity threshold.

        Returns:
            Collection of quotes ordered by semantic similarity.
        """
        query_embedding = self._embedder.embed(query)
        quotes = self._uow.quotes.find_similar(
            query_embedding, limit=limit, threshold=threshold
        )
        return Success(quotes)
