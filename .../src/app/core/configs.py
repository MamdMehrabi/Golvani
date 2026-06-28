from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Chat Application"
    DEBUG: bool = True

    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./chat.db"

settings = Settings()
