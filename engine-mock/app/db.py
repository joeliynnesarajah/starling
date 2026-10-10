"""SQLite setup for the Mock Engine Core.

Owner: Person 1
"""

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

DB_PATH = Path(__file__).resolve().parent.parent / "engine.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    """Create all tables if they don't exist yet."""
    from app import models  # noqa: F401  (registers the tables)

    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency: one database session per request."""
    with Session(engine) as session:
        yield session
