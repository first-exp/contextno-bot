from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_url: str 
    tg_token: str
    
    model_config = SettingsConfigDict(env_file=".env")

  
@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
    