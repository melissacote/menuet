import sqlite3

import pytest

from src import get_connection


def test_db_fk(conn: sqlite3.Connection) -> None:
    """Assert that foreign key enforcement is on."""
    result = conn.execute("PRAGMA foreign_keys").fetchone()
    assert result[0] == 1

def test_db_rowfactory(conn: sqlite3.Connection) -> None:
    """Assert that rows are returned as sqlite.Row objects."""
    result = conn.execute("SELECT 1 AS passing").fetchone()
    assert result["passing"] == 1

def test_db_conn_closes() -> None:
    """Check that connection closes after function execution."""
    with get_connection(":memory:") as c:
        pass
    with pytest.raises(sqlite3.ProgrammingError):
        c.execute("SELECT 1")

