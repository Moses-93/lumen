from abc import ABC, abstractmethod
from uuid import UUID

from lumen.domain.entities import Quote


class QuoteRepository(ABC):
    @abstractmethod
    def save(self, quote: Quote, embedding: list[float]) -> Quote:
        pass

    @abstractmethod
    def save_many(self, quotes: list[tuple[Quote, list[float]]]) -> list[Quote]:
        pass

    @abstractmethod
    def get_all(self) -> list[Quote]:
        pass

    @abstractmethod
    def get_by_id(self, quote_id: UUID) -> Quote | None:
        pass

    @abstractmethod
    def delete(self, quote_id: UUID) -> None:
        pass

    @abstractmethod
    def find_similar(self, embedding: list[float], limit: int = 1) -> list[Quote]:
        pass
