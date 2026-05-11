from __future__ import annotations

import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import ARRAY, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lumen.domain.entities import Note

from .base import BaseModel


class NoteModel(BaseModel):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(String(5000), nullable=False)
    moods: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    embedding: Mapped[NoteEmbeddingModel] = relationship(
        back_populates="note", uselist=False, cascade="all, delete-orphan"
    )

    @classmethod
    def from_entity(cls, note: Note, embedding: list[float]) -> NoteModel:
        return cls(
            id=note.id,
            text=note.text,
            moods=note.moods,
            embedding=NoteEmbeddingModel(embedding=embedding),
            created_at=note.created_at,
        )

    def to_entity(self) -> Note:
        return Note(
            id=self.id,
            text=self.text,
            moods=self.moods,
            created_at=self.created_at,
        )


class NoteEmbeddingModel(BaseModel):
    __tablename__ = "note_embeddings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    note_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    embedding: Mapped[list[float]] = mapped_column(Vector(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    note: Mapped[NoteModel] = relationship(back_populates="embedding")

    __table_args__ = (
        Index(
            "ix_note_embeddings_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )
