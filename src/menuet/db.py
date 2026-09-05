"""Database connection management."""

from pathlib import Path
from collections.abc import Generator
from sqlalchemy import create_engine, event, Engine, StaticPool
from sqlalchemy.engine import Connection

# Get project root and create data directory if it doesn't exist
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "menuet.db"
DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def create_db_engine(url: str) -> Engine:
    """Create an engine with foreign key enforcement enabled.
    In-memory databases for testing use StaticPool so all connections share one database."""
    if url == "sqlite://":
        new_engine = create_engine(url, poolclass=StaticPool, connect_args={"check_same_thread": False})
    else:
        new_engine = create_engine(url)

    @event.listens_for(new_engine, "connect")
    def _enable_foreign_keys(dbapi_conn, _connection_record):
        dbapi_conn.execute("PRAGMA foreign_keys = ON")

    return new_engine

engine = create_db_engine(f"sqlite:///{DEFAULT_DB_PATH}")

def get_connection() -> Generator[Connection]:
    """Yield a connection to the default database. The caller commits."""
    with engine.connect() as conn:
        yield conn


