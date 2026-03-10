from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    project_name: str = "API Tareas"
    api_prefix: str = "/api/v1"
    environment: str = "dev"

    # Database
    database_url: str

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()