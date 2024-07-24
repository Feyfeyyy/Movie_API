from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.movie import Base

load_dotenv(".env")

DATABASE_URL = environ.get(
    "DATABASE_URI", "postgresql://postgres:postgres@movies-db:5432/movies_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db_session() -> SessionLocal:
    """
    Get a database session

    :return: database session
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
