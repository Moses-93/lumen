from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from lumen.domain.repositories import NoteRepository
from lumen.domain.entities.note import Note
from lumen.infrastructure.persistence.postgres.models.note import NoteModel


class PostgresNoteRepository(NoteRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, note: Note, embedding: list[float]) -> Note:
        model = NoteModel.from_entity(note, embedding)
        self._session.add(model)
        self._session.flush()
        return note

    def delete(self, note_id: UUID) -> None:
        stmt = delete(NoteModel).where(NoteModel.id == note_id)
        self._session.execute(stmt)

    def get_by_id(self, note_id: UUID) -> Note | None:
        stmt = select(NoteModel).where(NoteModel.id == note_id)
        model = self._session.scalars(stmt).first()
        return model.to_entity() if model else None

    def get_all(self, limit: int = 10, offset: int = 0) -> list[Note]:
        stmt = (
            select(NoteModel)
            .order_by(NoteModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        models = self._session.scalars(stmt).all()
        return [m.to_entity() for m in models]
