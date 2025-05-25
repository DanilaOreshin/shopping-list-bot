from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    BOT_DEVELOPER: str
    BOT_VERSION: str
    BOT_TOKEN: str
    BOT_MASTER_PASSWORD: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    INTERVAL_CLEAR_MSG_HOURS: int
    INTERVAL_OLD_MSG_PERIOD: str

    @property
    def DATABASE_URL(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="resources/config_backup.env")


settings = BotSettings()
