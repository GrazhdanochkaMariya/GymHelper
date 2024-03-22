from typing import Any, List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Workout Tracker Project API"
    app_summary: str = (
        "Sport Goals Tracker is a FastAPI-based application"
        " designed to help users set and track their sports"
        " goals, such as running distance, gym workout sets,"
        " or workout duration. It utilizes websockets for"
        " real-time progress updates and Redis for caching"
        " progress and user statistics."
    )

    app_description: str = (
        "Sport Goals Tracker is a comprehensive application"
        " that allows users to set and track their fitness"
        " goals. It provides a user-friendly interface for"
        " creating scheduled workouts, tracking progress"
        " over time, and engaging with a community of"
        " like-minded individuals. The app also features"
        " a chat function for communication among users"
        " and a curated selection of articles on fitness"
        " and health topics."
    )

    # SECRET KEY IS USED FOR SECURING AUTH
    SECRET_KEY: str
    ALGORITHM: str

    # STARTUP MODE
    # e.g. PRODUCTION, DEBUG, TEST
    MODE: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database settings
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    TEST_DATABASE_NAME: str

    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str = ""
    CORS_HEADERS: list[str]

    # Timezone
    TZ: str

    # SMTP service
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: str

    # Broker
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    def get_async_database_url(self):
        database_url = (
            f"postgresql+asyncpg://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        return database_url

    def get_async_test_database_url(self):
        database_url = (
            f"postgresql+asyncpg://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.TEST_DATABASE_NAME}"
        )
        return database_url

    def get_database_url(self):
        database_url = (
            f"postgresql://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        return database_url


settings = Settings()

app_configs: dict[str, Any] = {
    "title": settings.app_name,
    "summary": settings.app_summary,
    "description": settings.app_description,
}
