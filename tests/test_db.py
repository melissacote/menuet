import sqlite3

import pytest

from src import get_connection


def test_db_fk(conn: sqlite3.Connection) -> None:
    """Assert that foreign key enforcement is on."""
    result = conn.execute("PRAGMA foreign_keys").fetchone()
    assert result[0] == 1
