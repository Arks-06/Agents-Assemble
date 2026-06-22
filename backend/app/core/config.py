from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agents Assemble"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

settings = Settings()