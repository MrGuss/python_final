"""
В этом файле вы описываете настройки приложения через pydantic-settings. Здесь вы читаете переменные окружения и формируете единый объект settings. Здесь должны быть значения APP_NAME, ENV, JWT_SECRET, JWT_ALG, ACCESS_TOKEN_EXPIRE_MINUTES, а также параметры БД, например SQLITE_PATH или DATABASE_URL. В этом файле не должно быть кода, который запускает приложение или выполняет запросы в БД. Только конфигурация.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    env: str

    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int

    sqlite_path: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
