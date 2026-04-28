from dishka import provide, Provider, Scope, FromComponent  # type: ignore

from typing import Annotated

from lumen.application.interfaces import Embedder, UnitOfWork
from lumen.application.use_cases import SeedQuotesInteractor, FindQuotesInteractor


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
