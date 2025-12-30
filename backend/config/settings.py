from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class _BaseSettings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


class RAGSettings(_BaseSettings):
    app_name: str = Field(default="fullstack_rag_com")
    openai_api_key: str = Field(default="", repr=False)
    openai_model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-3-small")
    docs_path: Path = Field(default=Path(__file__).resolve().parents[2] / "docs")
    chroma_dir: Path = Field(default=Path(__file__).resolve().parents[1] / "chroma_db")
    chunk_size: int = Field(default=800)
    chunk_overlap: int = Field(default=100)
    k_results: int = Field(default=5)
    temperature: float = Field(default=0.1)


class DatabaseSettings(_BaseSettings):
    drivername: str = Field(description="Database driver name")
    username: str = Field(description="Database username")
    password: str = Field(description="Database password", repr=False)
    host: str = Field(description="Database host")
    port: int = Field(description="Database port")
    database: str = Field(description="Database name")

class LoginSettings(_BaseSettings):
    jwt_secret_key: str = Field(default="change_me", repr=False)
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)


@lru_cache()
def get_rag_settings() -> RAGSettings:
    return RAGSettings()


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


@lru_cache()
def get_login_settings() -> LoginSettings:
    return LoginSettings()
