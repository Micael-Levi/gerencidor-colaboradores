import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Gerencia configurações principais"""

    database_name: str = os.getenv("DATABASE_NAME", "banco_colaboradores")
    database_host: str = os.getenv("DATABASE_HOST", "localhost")
    database_port: str = os.getenv("DATABASE_PORT", "5432")
    database_user: str = os.getenv("DATABASE_USER", "postgres")
    database_password: str = os.getenv("DATABASE_PASSWORD", "postgres123")

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"


settings = Settings()
