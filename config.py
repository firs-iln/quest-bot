from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    TOKEN: SecretStr
    QUEST_STEP: int

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


# class QuestConfig(BaseSettings):
#     # YESCOIN_CHANNEL: str
#     # CHAT_WITH_AGENT: str
#
#     model_config = SettingsConfigDict(env_file='quest.env', env_file_encoding='utf-8')


config = Settings()
# quest_config = QuestConfig()
