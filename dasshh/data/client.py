from pathlib import Path
from typing import Generator

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class DBClient:
    """Dasshh database client."""

    db_path = Path.home() / ".dasshh" / "db" / "dasshh.db"

    def __init__(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine: Engine = create_engine(f"sqlite:///{self.db_path}")
        self.DatabaseSessionFactory: sessionmaker = sessionmaker(bind=self.engine)

        Base.metadata.create_all(bind=self.engine)

    def get_db(self) -> Generator[Session, None, None]:
        """Get a database session."""
        db: Session = self.DatabaseSessionFactory()
        return db
