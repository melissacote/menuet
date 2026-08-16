"""Database connection management."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from collections.abc import Generator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "menuet.db"

@contextmanager
def get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> Generator[sqlite3.Connection]:
    """Yield a configured SQLite database connection.

    Foreign keys are enabled and rows are returned as sqlite3.Row.
    The caller of the connection commits.
    """

    # Create directory if it does not already exist
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)

    # Configure connection
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()