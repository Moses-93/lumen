from __future__ import annotations

import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import ARRAY, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lumen.domain.entities import Quote

from .base import BaseModel


class QuoteModel(BaseModel):
    __tablename__ = "quotes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255))
    source: Mapped[str | None] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    embedding: Mapped[QuoteEmbeddingModel] = relationship(
        back_populates="quote", uselist=False, cascade="all, delete-orphan"
    )

    @classmethod
    def from_entity(cls, quote: Quote, embedding: list[float]) -> QuoteModel:
        return cls(
            id=quote.id,
            author=str(quote.author),
            domain=quote.domain,
            source=quote.source,
            text=str(quote.text),
            tags=quote.tags,
            embedding=QuoteEmbeddingModel(embedding=embedding),
            created_at=quote.created_at,
            updated_at=quote.updated_at,
        )

    def to_entity(self) -> Quote:
        return Quote.reconstruct(
            id=self.id,
            author=self.author,
            domain=self.domain,
            source=self.source,
            text=self.text,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class QuoteEmbeddingModel(BaseModel):
    __tablename__ = "quote_embeddings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quote_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quotes.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    embedding: Mapped[list[float]] = mapped_column(Vector(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    quote: Mapped[QuoteModel] = relationship(back_populates="embedding")

    __table_args__ = (
        Index(
            "ix_quote_embeddings_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )
