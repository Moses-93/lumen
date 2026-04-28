from lumen.application.dtos import Success, Result, AddNoteCommand
from lumen.application.interfaces import Embedder, UnitOfWork
from lumen.domain.entities import Quote


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
