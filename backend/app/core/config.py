import secrets
from typing import Annotated
from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(
        default="",
        description="OpenAI API Key - Required for AI features",
    )

    # Clerk Configuration
    CLERK_SECRET_KEY: str = Field(
        default="",
        description="Clerk Secret Key - Required for authentication",
    )
    JWKS_PUBLIC_KEY: str = Field(
        default="",
        description="Clerk JWKS Public Key - Required for JWT verification",
    )

    PROJECT_NAME: str = "Questions API"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432  # PostgreSQL docker容器内部端口5432，本地主机访问端口5433
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "questions_db"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()

