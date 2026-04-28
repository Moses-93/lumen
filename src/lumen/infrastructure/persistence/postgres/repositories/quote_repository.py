from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from lumen.domain.entities import Quote
from lumen.domain.repositories import QuoteRepository
from lumen.infrastructure.persistence.postgres.models import (
    QuoteModel,
    QuoteEmbeddingModel,
)


class PostgresQuoteRepository(QuoteRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, quote: Quote, embedding: list[float]) -> Quote:
        model = QuoteModel.from_entity(quote, embedding)
        self._session.merge(model)
        self._session.flush()

        return quote

    def save_many(self, quotes: list[tuple[Quote, list[float]]]) -> list[Quote]:
        models = [
            QuoteModel.from_entity(quote, embedding) for quote, embedding in quotes
        ]
        self._session.add_all(models)
        self._session.flush()

        return [quote for quote, _ in quotes]

    def delete(self, quote_id: UUID) -> None:
        stmt = delete(QuoteModel).where(QuoteModel.id == quote_id)
        self._session.execute(stmt)

    def get_by_id(self, quote_id: UUID) -> Quote | None:
        stmt = select(QuoteModel).where(QuoteModel.id == quote_id)
        model = self._session.scalars(stmt).first()
        return model.to_entity() if model else None

    def get_all(self) -> list[Quote]:
        stmt = select(QuoteModel).order_by(QuoteModel.created_at.desc())
        models = self._session.scalars(stmt).all()
        return [m.to_entity() for m in models]

    def find_similar(
        self, embedding: list[float], limit: int = 1, threshold: float = 0.28
    ) -> list[Quote]:
        distance = QuoteEmbeddingModel.embedding.cosine_distance(embedding)
        stmt = (
            select(QuoteModel)
            .join(QuoteEmbeddingModel)
            .where(distance < threshold)
            .order_by(distance)
            .limit(limit)
        )
        models = self._session.scalars(stmt).all()
        return [m.to_entity() for m in models]
