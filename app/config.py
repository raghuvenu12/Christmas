from functools import lru_cache
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Citizen"
    APP_VERSION: str = "0.1.0"
    max_otp_attempts:int =3

    class Config:
        env_file = os.getenv('ENV_FILE', 'local.env')
        extra = 'allow'


@lru_cache()
def get_settings():
    print(Settings().dict())
    return Settings()