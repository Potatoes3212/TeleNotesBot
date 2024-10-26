import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Параметры для подключения к БД
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Указываем файл окружения
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), ".env"),
        env_file_encoding='utf-8',
        extra="ignore"
    )

    # Метод для создания строки подключения к базе данных
    def get_db_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


# Создаём экземпляр настроек, который загрузит данные из .env
settings = Settings()

# DATABASE_URL = settings.get_db_url()
# print(DATABASE_URL)
