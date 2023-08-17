import pytest
from fastapi.testclient import TestClient
from typing import Generator
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from api.index import app
from database.get_db import DATABASE_URL

@pytest.fixture(scope="function")
def client() -> Generator:
    """
    Create a test client for the FastAPI app.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture
def context():

    """
    Variable to store context data between steps.
    Note: remember to always return the context variable at the end of the each steps.
    """
    b = {}
    yield b

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

