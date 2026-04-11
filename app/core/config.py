from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Tender AI"
    app_env: str = "local"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/tender_ai"
    redis_url: str = "redis://localhost:6379/0"
    llm_api_key: str = ""
    llm_base_url: str = ""
    rustfs_endpoint: str = ""
    rustfs_access_key: str = ""
    rustfs_secret_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
