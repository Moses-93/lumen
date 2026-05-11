from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide  # type: ignore

from lumen.application.interfaces import Embedder, UnitOfWork
from lumen.application.use_cases import (
    AddNoteInteractor,
    FindQuotesInteractor,
    FindSimilarNotesInteractor,
    GetNotesInteractor,
    SeedQuotesInteractor,
)


class UseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def seed_quotes(
        self,
        embedder: Annotated[Embedder, FromComponent("passage")],
        uow: UnitOfWork,
    ) -> SeedQuotesInteractor:
        return SeedQuotesInteractor(embedder, uow)

    @provide(scope=Scope.REQUEST)
    def find_quotes(
        self,
        embedder: Annotated[Embedder, FromComponent("query")],
        uow: UnitOfWork,
    ) -> FindQuotesInteractor:
        return FindQuotesInteractor(embedder, uow)

    @provide(scope=Scope.REQUEST)
    def add_note(
        self,
        passage_embedder: Annotated[Embedder, FromComponent("passage")],
        query_embedder: Annotated[Embedder, FromComponent("query")],
        uow: UnitOfWork,
    ) -> AddNoteInteractor:
        return AddNoteInteractor(
            uow,
            passage_embedder=passage_embedder,
            query_embedder=query_embedder,
        )

    @provide(scope=Scope.REQUEST)
    def get_notes(
        self,
        uow: UnitOfWork,
    ) -> GetNotesInteractor:
        return GetNotesInteractor(uow)

    @provide(scope=Scope.REQUEST)
    def find_similar_notes(
        self,
        query_embedder: Annotated[Embedder, FromComponent("query")],
        uow: UnitOfWork,
    ) -> FindSimilarNotesInteractor:
        return FindSimilarNotesInteractor(uow, query_embedder=query_embedder)
