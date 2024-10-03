from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд'
    database_url: str = 'sqqlite+aiosqlite:///./sqlite3.db'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
