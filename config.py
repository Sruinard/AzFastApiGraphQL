import os

from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
	POSTGRESDB_URL: str
	IS_DEBUG: bool

	class Config:
		env_file = ".env"

@lru_cache()
def load_config():
	return Settings()