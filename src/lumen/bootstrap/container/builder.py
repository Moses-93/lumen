from dishka import Container, Provider, Scope, make_container, provide  # type: ignore

from lumen.config import Settings

from .application import application_providers
from .infrastructure import infrastructure_providers


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
