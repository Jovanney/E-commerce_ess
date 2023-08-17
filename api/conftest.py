import pytest
from fastapi.testclient import TestClient
from typing import Generator
from api.index import app

@pytest.fixture(scope="function")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture
def context():
    b = {}
    yield b