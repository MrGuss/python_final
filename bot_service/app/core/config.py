from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    env: str

    telegram_bot_token: str

    jwt_secret: str
    jwt_alg: str

    redis_url: str
    rabbitmq_url: str

    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str
    http_proxy: str | None = None

    model_config = SettingsConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
