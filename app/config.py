from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    API_KEY: str = ""
    VALID_API_KEYS: str = ""
    OPENAI_API_KEY: str
    FAISS_INDEX_PATH: str = "data/index.faiss"
    DOCSTORE_PATH: str = "data/docstore.json"
    MODEL_NAME: str = "paraphrase-multilingual-mpnet-base-v2"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
