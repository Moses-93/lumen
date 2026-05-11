from lumen.application.dtos import (
    AddNoteCommand,
    FindSimilarNotesQuery,
    GetNotesQuery,
    Result,
    Success,
)
from lumen.application.interfaces import Embedder, UnitOfWork
from lumen.domain.entities import Note, Quote


class AddNoteInteractor:
    """Orchestrates note creation."""

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
        """Persists a new note and retrieves semantically similar quotes.

        Args:
            command: Input data for the new note.

        Returns:
            Collection of quotes matching the note's context.
        """
        note = command.to_entity()

        passage_embedding = self._passage_embedder.embed(note.text)
        query_embedding = self._query_embedder.embed(note.text)

        with self._uow.transaction():
            self._uow.notes.add(note, passage_embedding)
            resonant_quotes = self._uow.quotes.find_similar(embedding=query_embedding)
            self._uow.save()

        return Success(resonant_quotes)


class GetNotesInteractor:
    """Orchestrates temporal and paginated note retrieval."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def execute(self, query: GetNotesQuery) -> Result[list[Note]]:
        """Retrieves notes matching the specified query filters.

        Args:
            query: Parameters for filtering and pagination.

        Returns:
            Collection of notes matching the query.
        """
        with self._uow.transaction():
            notes = self._uow.notes.get_all(
                limit=query.limit,
                from_date=query.from_date,
                to_date=query.to_date,
            )
        return Success(notes)


class FindSimilarNotesInteractor:
    """Orchestrates semantic search across existing notes."""

    def __init__(
        self,
        uow: UnitOfWork,
        *,
        query_embedder: Embedder,
    ) -> None:
        self._uow = uow
        self._query_embedder = query_embedder

    def execute(self, query: FindSimilarNotesQuery) -> Result[list[Note]]:
        """Finds notes semantically similar to the provided query text.

        Args:
            query: Search parameters and input text.

        Returns:
            Collection of notes ordered by semantic similarity.
        """
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
