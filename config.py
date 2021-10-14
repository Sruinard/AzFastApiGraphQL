import os

from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
        POSTGRESDB_URL: str
        IS_DEBUG: bool

@lru_cache()
def load_config():
        return Settings(
                POSTGRESDB_URL=os.environ.get("POSTGRESDB_URL", "sqlite:///develop.db"),
                IS_DEBUG=os.environ.get("IS_DEBUG", False)
        )