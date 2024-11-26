from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv('config.py')

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()

engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

