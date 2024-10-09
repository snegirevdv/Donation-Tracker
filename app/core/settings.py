from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings configuration."""

    app_title: str = 'Donation Tracker'
    app_description: str = (
        'A platform for managing charity and '
        'fundraising projects, along with donations.'
    )
    database_url: str = 'sqlite+aiosqlite:///./sqlite3.db'
    secret_key: str = 'basic_secret_key'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
