from sqlalchemy import Connection, text

def test_db_fk(conn: Connection) -> None:
    """Assert that foreign key enforcement is on."""
    result = conn.execute(text("PRAGMA foreign_keys")).fetchone()
    assert result[0] == 1
