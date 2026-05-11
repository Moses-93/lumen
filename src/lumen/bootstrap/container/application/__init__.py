from dishka import Provider

from .use_cases import UseCasesProvider


def application_providers() -> list[Provider]:
    return [UseCasesProvider()]
