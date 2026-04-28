from dishka import Container, Provider, Scope, provide, make_container  # type: ignore

from lumen.config import Settings

from .infrastructure import infrastructure_providers
from .application import application_providers


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide()
    def settings(self) -> Settings:
        return Settings()  # type: ignore


def build_container() -> Container:
    return make_container(
        SettingsProvider(),
        *infrastructure_providers(),
        *application_providers(),
    )
