from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"  # Specify the path to your .env file

app_settings = AppSettings()

