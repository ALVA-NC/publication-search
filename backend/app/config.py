
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openalex_api_key: str

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "publication_search"
    mongodb_collection: str = "publications"

    elasticsearch_url: str = "http://localhost:9200"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
