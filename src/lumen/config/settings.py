from pathlib import Path
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    embedding_model: str = Field(alias="EMBEDDING_MODEL")
    embedding_cache_dir: Path | None = Field(alias="EMBEDDING_CACHE_DIR", default=None)
    embedding_batch_size: int = Field(alias="EMBEDDING_BATCH_SIZE", default=128)
    use_gpu: bool = Field(alias="USE_GPU", default=False)
    llm_model: str = Field(alias="LLM_MODEL")

    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")

    def postgres_url(self, driver: str = "psycopg") -> str:
        return (
            f"postgresql+{driver}://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
