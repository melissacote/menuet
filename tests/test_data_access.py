from sqlalchemy import Connection, select
from menuet.data_access.sources import get_or_create_source_url
from menuet.schema import sources


def test_get_or_create_source_url(conn: Connection) -> None:
    """
    Assert that get_or_create_source_url adds a new url source to the database.
    """
    source_id = get_or_create_source_url(conn, "https://www.example.com/recipe")
    row = conn.execute(select(sources).where(sources.c.source_id == source_id)).one()
    assert row.source_type == "url"
    assert row.url == "https://www.example.com/recipe"

def test_get_or_create_source_url_duplicates(conn: Connection) -> None:
    """
    Assert that get_or_create_source_url returns the correct id for a duplicate.
    """
    source_id = get_or_create_source_url(conn, "https://www.example.com/recipe")
    duplicate_source_id = get_or_create_source_url(conn, "https://www.example.com/recipe")
    assert source_id == duplicate_source_id

def test_get_or_create_source_url_case_insensitive(conn: Connection) -> None:
    """
    Assert that get_or_create_source_url duplicate check is not case-sensitive.
    """
    source_id = get_or_create_source_url(conn, "https://www.example.com/Recipe")
    duplicate_source_id = get_or_create_source_url(conn, "https://www.example.com/recipe")
    assert source_id == duplicate_source_id

def test_get_or_create_source_url_whitespace(conn: Connection) -> None:
    """
    Assert that get_or_create_source_url correctly ignores whitespace for duplicate checks.
    """
    source_id = get_or_create_source_url(conn, "https://www.example.com/recipe ")
    duplicate_source_id = get_or_create_source_url(conn, "https://www.example.com/recipe")
    assert source_id == duplicate_source_id

def test_get_or_create_source_url_original_preserved(conn: Connection) -> None:
    """
    Assert that get_or_create_source_url preserves the original formatting of the URL.
    """
    source_id = get_or_create_source_url(conn, "https://www.example.com/Recipe")
    row = conn.execute(select(sources.c.url).where(sources.c.source_id == source_id)).one()
    assert row.url == "https://www.example.com/Recipe"