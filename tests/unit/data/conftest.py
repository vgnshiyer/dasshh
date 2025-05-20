"""
Test fixtures for the data module.
"""
import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dasshh.data.client import Base, DBClient
from dasshh.data.session import SessionService


@pytest.fixture
def test_db_file():
    """Create a temporary database file."""
    fd, path = tempfile.mkstemp()
    try:
        yield path
    finally:
        os.close(fd)
        os.unlink(path)


@pytest.fixture
def test_db_client(monkeypatch, test_db_file):
    """Create a test database client with a temporary database."""
    class TestDBClient(DBClient):
        def __init__(self, db_path):
            self.db_path = db_path
            self.engine = create_engine(f"sqlite:///{self.db_path}")
            self.DatabaseSessionFactory = sessionmaker(bind=self.engine)
            Base.metadata.create_all(bind=self.engine)

    client = TestDBClient(test_db_file)
    return client


@pytest.fixture
def test_session_service(test_db_client):
    """Create a test session service."""
    return SessionService(test_db_client)
