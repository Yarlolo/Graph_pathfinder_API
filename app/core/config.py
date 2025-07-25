from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CELERY_BROKER_URL: str = "sqla+sqlite:///celery.db?check_same_thread=False"
    CELERY_RESULT_BACKEND: str = "db+sqlite:///results.db?check_same_thread=False"

    class Config:
        env_file = '.env'

settings = Settings()