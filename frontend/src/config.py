from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Resolve path to the .env file in the frontend root
env_path = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    BACKEND_URL: str = "http://localhost:8000"
    
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

settings = Settings()