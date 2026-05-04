from lumen.application.dtos import (
    Success,
    Result,
    AddNoteCommand,
    GetNotesQuery,
    FindSimilarNotesQuery,
)
from lumen.application.interfaces import Embedder, UnitOfWork
from lumen.domain.entities import Quote, Note


class AddNoteInteractor:
    def __init__(
        self,
        uow: UnitOfWork,
        *,
        passage_embedder: Embedder,
        query_embedder: Embedder,
    ) -> None:
        self._passage_embedder = passage_embedder
        self._query_embedder = query_embedder
        self._uow = uow

    def execute(self, command: AddNoteCommand) -> Result[list[Quote]]:
        """Executes the add note command."""
        note = command.to_entity()

        passage_embedding = self._passage_embedder.embed(note.text)
        query_embedding = self._query_embedder.embed(note.text)

        with self._uow.transaction():
            self._uow.notes.add(note, passage_embedding)
            resonant_quotes = self._uow.quotes.find_similar(embedding=query_embedding)
            self._uow.save()

        return Success(resonant_quotes)


class GetNotesInteractor:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def execute(self, query: GetNotesQuery) -> Result[list[Note]]:
        with self._uow.transaction():
            notes = self._uow.notes.get_all(
                limit=query.limit,
                from_date=query.from_date,
                to_date=query.to_date,
            )
        return Success(notes)


class FindSimilarNotesInteractor:
    def __init__(
        self,
        uow: UnitOfWork,
        *,
        query_embedder: Embedder,
    ) -> None:
        self._uow = uow
        self._query_embedder = query_embedder

    def execute(self, query: FindSimilarNotesQuery) -> Result[list[Note]]:
        embedding = self._query_embedder.embed(query.text)

        with self._uow.transaction():
            notes = self._uow.notes.find_similar(
                embedding=embedding,
                limit=query.limit,
                threshold=query.threshold,
                from_date=query.from_date,
                to_date=query.to_date,
            )

        return Success(notes)
