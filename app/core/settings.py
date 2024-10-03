from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = 'Сервис бронирования переговорных комнат'
    database_url: str = 'sqqlite+aiosqlite:///./sqlite3.db'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
