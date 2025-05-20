"""
Tests for the database client.
"""
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from dasshh.data.client import DBClient


def test_db_client_initialization():
    """Test creating a DBClient instance."""
    client = DBClient()
    assert client.db_path.parent.exists()
    assert isinstance(client.engine, Engine)
    assert client.DatabaseSessionFactory is not None


def test_db_client_get_db(test_db_client):
    """Test getting a database session."""
    db = test_db_client.get_db()
    assert db is not None
    assert isinstance(db, Session)


def test_db_client_get_db_as_context_manager(test_db_client):
    """Test using the database session as a context manager."""
    with test_db_client.get_db() as db:
        assert db is not None
        assert isinstance(db, Session)
