import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = os.getenv(
        "DB_URL",
        "postgresql+asyncpg://postgres:567234@localhost:5432/contacts_db",
    )

settings = Settings()
