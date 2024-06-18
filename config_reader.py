from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token_bot: SecretStr
    redis_url: str
    contextno_url: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
