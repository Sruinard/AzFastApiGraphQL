import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv

dotenv.load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get("DB_CONN")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()