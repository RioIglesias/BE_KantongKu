from typing import Literal
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env'), env_ignore_empty=True
    )
    
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DB_URL: AnyUrl # it should be read by .env
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 
    # 60 minutes * 24 hours * 8 days = 8 days
    
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',] = "INFO"
    
    
config = Settings()
print(str(config.DB_URL))