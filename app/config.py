from pydantic_settings import BaseSettings
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo  # Добавляем импорт для ValidationInfo

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL", mode="before") #Параметр mode="before" указан, чтобы значение DATABASE_URL формировалось до валидации.
    def assemble_db_url(cls, v, values: ValidationInfo):  # Указываем тип values как ValidationInfo
        data = values.data  # Доступ к данным через `.data`
        return (
            f"postgresql+asyncpg://{data['DB_USER']}:{data['DB_PASS']}"
            f"@{data['DB_HOST']}:{data['DB_PORT']}/{data['DB_NAME']}"
        )

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()

