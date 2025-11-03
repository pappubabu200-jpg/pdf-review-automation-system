from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    X_SECRET: str
    TELEGRAM_BOT_TOKEN: str
    N8N_WEBHOOK_URL: str
    BASE_URL: str
    FILES_PATH: str = "./static/files"
    MAX_UPLOAD_MB: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
Path(settings.FILES_PATH).mkdir(parents=True, exist_ok=True)
