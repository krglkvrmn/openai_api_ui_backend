import os
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Self

from pydantic import (
    AliasChoices, BaseModel, DirectoryPath, Field, HttpUrl, PositiveInt, PostgresDsn, SecretStr,
    model_validator
)
from pydantic_core.core_schema import ValidationInfo, ValidatorFunctionWrapHandler
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(os.getenv('ENV_FILE'))
SECRETS_DIR = Path(os.getenv('SECRETS_DIR'))


class OAuth2Config(BaseModel):
    CLIENT_ID: SecretStr
    CLIENT_SECRET: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        secrets_dir=SECRETS_DIR,
        extra="ignore",
        validate_default=True,
        case_sensitive=False
    )

    # Project
    APP_ROOT: DirectoryPath = Field(default_factory=lambda: Path(__file__).parent.parent)
    PROJECT_ROOT: DirectoryPath = Field(default_factory=lambda: Path(__file__).parent.parent.parent)

    ENV_TYPE: Literal["DEV", "PROD"] = "DEV"

    # Host
    APP_LOCAL_HOST: str = 'localhost'
    APP_LOCAL_PORT: int = Field(default=8000, ge=0, le=65535)
    APP_PUBLIC_DOMAIN: Optional[str] = None
    APP_ORIGIN: HttpUrl
    MAIN_PAGE_URL: HttpUrl = "http://localhost:3001"

    OPENAPI_URL: str = '/openapi.json'

    # OpenAI API config
    OPENAI_API_ENDPOINTS: Dict[str, Dict[str, str]] = {
        "completions": {"method": "POST", "url": "https://api.openai.com/v1/chat/completions"}
    }

    # Postgres credentials
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = Field(default=5432, ge=0, le=65535)
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_ENGINE: str = 'asyncpg'
    DATABASE_URL: PostgresDsn

    # Redis credentials
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = Field(default=6379, ge=0, le=65535)

    # Crypto-keys
    ACCESS_TOKEN_SECRET: SecretStr
    REFRESH_TOKEN_SECRET: SecretStr
    VERIFICATION_TOKEN_SECRET: SecretStr
    RESET_PASSWORD_TOKEN_SECRET: SecretStr
    KEY_ENCODE_SECRET: SecretStr

    # Sendgrid
    SENDGRID_API_KEY: SecretStr

    # Oauth2 client credentials
    GOOGLE_OAUTH_CONFIG: OAuth2Config
    GITHUB_OAUTH_CONFIG: OAuth2Config = Field(
        validation_alias=AliasChoices('github_oauth_config_local', 'github_oauth_config')
    )

    # Lifetimes configuration
    # Tokens lifetimes
    ACCESS_TOKEN_LIFETIME: PositiveInt = 60 * 60
    REFRESH_TOKEN_LIFETIME: PositiveInt = 60 * 60 * 2
    VERIFICATION_TOKEN_LIFETIME: PositiveInt = 60 * 10

    # Cookies lifetimes
    ACCESS_TOKEN_COOKIE_LIFETIME: PositiveInt = 60 * 60 * 2
    REFRESH_TOKEN_COOKIE_LIFETIME: PositiveInt = 60 * 60 * 2

    # Accounts lifetimes
    GUEST_ACCOUNT_LIFETIME: PositiveInt = 60
    UNVERIFIED_ACCOUNT_LIFETIME: PositiveInt = 60 * 3


    @model_validator(mode='before')
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        if data.get('ENV_TYPE') == 'PROD':
            assert data.get('APP_PUBLIC_DOMAIN') is not None
            data['APP_ORIGIN'] = f'https://{data["APP_PUBLIC_DOMAIN"]}'
            data['MAIN_PAGE_URL'] = data['APP_ORIGIN']
        else:
            data['APP_ORIGIN'] = f'http://{data["APP_LOCAL_HOST"]}:{data["APP_LOCAL_PORT"]}'

        data['DATABASE_URL'] = (
            f'postgresql+{data["POSTGRES_ENGINE"]}://{data["POSTGRES_USER"]}:'
            f'{data["POSTGRES_PASSWORD"]}@{data["POSTGRES_HOST"]}/{data["POSTGRES_DB"]}'
        )

        return data


settings = Settings()
