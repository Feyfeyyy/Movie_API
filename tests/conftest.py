from os import environ
import random
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db_session
from app.models.movie import Base, Movie
from app.routes.movie_info import router as movie_router
from app.routes.ratings import router as rating_router


def start_application():
    app = FastAPI()
    app.include_router(movie_router)
    app.include_router(rating_router)
    return app


# SQLite database URL for testing
TEST_DATABASE_URL = environ.get(
    "TEST_DATABASE_URL", "postgresql://postgres:postgres@movies-db:5432/movies_db"
)

# Create a SQLAlchemy engine
engine = create_engine(TEST_DATABASE_URL, echo=False, poolclass=StaticPool)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(
    expire_on_commit=False, autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture()
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(
        app: FastAPI, db_session: TestingSessionLocal
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db_session` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db_session] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def create_single_mock_movie():
    mock_movie = Movie(
        id=random.randint(1, 5),
        user_id=random.randint(1, 5),
        title="Mock Movie Title",
        genre="Mock Movie Genre",
        year=random.randint(2000, 2021),
        runtime=f"{random.randint(90, 180)} min",
        rating=random.randint(1, 5),
        avr_rating=random.randint(1, 5),
    )
    return mock_movie


@pytest.fixture()
def create_mock_movie_list():
    mock_movie_list = []
    for i in range(5):
        mock_movie_list.append(
            Movie(
                id=i,
                user_id=random.randint(1, 5),
                title=f"Mock Movie Title {i}",
                genre="Mock Movie Genre",
                year=random.randint(2000, 2021),
                runtime=f"{random.randint(90, 180)} min",
                rating=random.randint(1, 5),
                avr_rating=random.randint(1, 5),
            )
        )
    return mock_movie_list
