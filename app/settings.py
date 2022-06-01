import multiprocessing

from decouple import AutoConfig
from pydantic import BaseSettings

config = AutoConfig()


class Settings(BaseSettings):
    API_TOKEN: str = config("API_TOKEN")
    NUM_THREADS: int = config(
        "NUM_THREADS", default=multiprocessing.cpu_count()
    )
    I18N_PATH: str = config("I18N_PATH")
    DB_URI: str = config("DB_URI")
    DB_NAME: str = config("DB_NAME")
    DB_COLLECTION: str = config("DB_COLLECTION")


settings = Settings()
