"""应用配置定义。"""

from pydantic import BaseModel, Field, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """数据库配置。"""

    host: str
    port: int
    db: str
    user: str
    password: str
    url: str


class RedisSettings(BaseModel):
    """Redis 配置。"""

    url: str


class LlmSettings(BaseModel):
    """大模型配置。"""

    api_key: str
    base_url: str
    model: str


class RustFsSettings(BaseModel):
    """rustfs 配置。"""

    endpoint: str
    access_key: str
    secret_key: str
    bucket: str


class Settings(BaseSettings):
    """应用顶层配置。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    app_name: str = Field(default="Tender AI", validation_alias="APP_NAME")
    app_env: str = Field(default="local", validation_alias="APP_ENV")
    app_debug: bool = Field(default=True, validation_alias="APP_DEBUG")
    app_host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    app_port: int = Field(default=8000, validation_alias="APP_PORT")
    auth_secret_key: str = Field(default="dev-secret-key", validation_alias="AUTH_SECRET_KEY")
    auth_access_token_expire_seconds: int = Field(
        default=7200,
        validation_alias="AUTH_ACCESS_TOKEN_EXPIRE_SECONDS",
    )

    postgres_host: str = Field(default="", validation_alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    postgres_db: str = Field(default="", validation_alias="POSTGRES_DB")
    postgres_user: str = Field(default="", validation_alias="POSTGRES_USER")
    postgres_password: str = Field(default="", validation_alias="POSTGRES_PASSWORD")
    database_url: str = Field(default="", validation_alias="DATABASE_URL")

    redis_url: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="REDIS_URL",
    )

    llm_api_key: str = Field(default="", validation_alias="LLM_API_KEY")
    llm_base_url: str = Field(default="", validation_alias="LLM_BASE_URL")
    llm_model: str = Field(default="", validation_alias="LLM_MODEL")

    rustfs_endpoint: str = Field(default="", validation_alias="RUSTFS_ENDPOINT")
    rustfs_access_key: str = Field(default="", validation_alias="RUSTFS_ACCESS_KEY")
    rustfs_secret_key: str = Field(default="", validation_alias="RUSTFS_SECRET_KEY")
    rustfs_bucket: str = Field(default="", validation_alias="RUSTFS_BUCKET")

    @model_validator(mode="after")
    def build_database_url(self) -> "Settings":
        """当未显式传入 DATABASE_URL 时自动拼接连接串。"""
        if self.database_url:
            return self

        if not all(
            [
                self.postgres_host,
                self.postgres_db,
                self.postgres_user,
                self.postgres_password,
            ]
        ):
            return self

        self.database_url = (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        return self

    @computed_field
    @property
    def database(self) -> DatabaseSettings:
        """聚合数据库配置。"""
        return DatabaseSettings(
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            url=self.database_url,
        )

    @computed_field
    @property
    def redis(self) -> RedisSettings:
        """聚合 Redis 配置。"""
        return RedisSettings(url=self.redis_url)

    @computed_field
    @property
    def llm(self) -> LlmSettings:
        """聚合大模型配置。"""
        return LlmSettings(
            api_key=self.llm_api_key,
            base_url=self.llm_base_url,
            model=self.llm_model,
        )

    @computed_field
    @property
    def rustfs(self) -> RustFsSettings:
        """聚合 rustfs 配置。"""
        return RustFsSettings(
            endpoint=self.rustfs_endpoint,
            access_key=self.rustfs_access_key,
            secret_key=self.rustfs_secret_key,
            bucket=self.rustfs_bucket,
        )


settings = Settings()
