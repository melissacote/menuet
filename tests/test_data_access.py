from sqlalchemy import Connection, select
from menuet.data_access.sources import get_or_create_source_url, get_or_create_source_book, get_or_create_source_other
from menuet.schema import sources

# region url tests
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
# endregion url tests

# region book tests
def test_get_or_create_source_book(conn: Connection) -> None:
    """
    Assert that get_or_create_source_book adds a new book source to the database.
    """
    source_id = get_or_create_source_book(conn, "Test Book", "Test Author")
    row = conn.execute(select(sources).where(sources.c.source_id == source_id)).one()
    assert row.source_type == "book"
    assert row.book_title == "Test Book"
    assert row.book_author == "Test Author"


def test_get_or_create_source_book_returns_existing_duplicate(conn: Connection) -> None:
    """
    Assert that a book matching an existing title and author (ignoring case and
    surrounding whitespace) returns the existing source_id.
    """
    first_id = get_or_create_source_book(conn, "  TEST book ", " test AUTHOR  ")
    second_id = get_or_create_source_book(conn, "Test Book", "Test Author")
    assert first_id == second_id


def test_get_or_create_source_book_same_title_different_author(conn: Connection) -> None:
    """
    Assert that a book with the same title but a different author is a new source.
    """
    first_id = get_or_create_source_book(conn, "Test Book", "Author One")
    second_id = get_or_create_source_book(conn, "Test Book", "Author Two")
    assert first_id != second_id


def test_get_or_create_source_book_same_author_different_title(conn: Connection) -> None:
    """
    Assert that a book with the same author but a different title is a new source.
    """
    first_id = get_or_create_source_book(conn, "Book One", "Test Author")
    second_id = get_or_create_source_book(conn, "Book Two", "Test Author")
    assert first_id != second_id


def test_get_or_create_source_book_stores_as_given(conn: Connection) -> None:
    """
    Assert that the title and author are stored exactly as given, not normalized.
    """
    source_id = get_or_create_source_book(conn, "  TEST book ", " test AUTHOR  ")
    row = conn.execute(select(sources).where(sources.c.source_id == source_id)).one()
    assert row.book_title == "  TEST book "
    assert row.book_author == " test AUTHOR  "
# endregion book tests

# region other tests
def test_get_or_create_source_other(conn: Connection) -> None:
    """
    Assert that get_or_create_source_other adds a new other source to the database.
    """
    source_id = get_or_create_source_other(conn, "Memaw's recipe card")
    row = conn.execute(select(sources).where(sources.c.source_id == source_id)).one()
    assert row.source_type == "other"
    assert row.description == "Memaw's recipe card"


def test_get_or_create_source_other_returns_existing_duplicate(conn: Connection) -> None:
    """
    Assert that a description matching an existing one (ignoring case and
    surrounding whitespace) returns the existing source_id.
    """
    first_id = get_or_create_source_other(conn, "  MEMAW'S recipe Card ")
    second_id = get_or_create_source_other(conn, "Memaw's recipe card")
    assert first_id == second_id


def test_get_or_create_source_other_different_description(conn: Connection) -> None:
    """
    Assert that a different description is a new source.
    """
    first_id = get_or_create_source_other(conn, "Memaw's recipe card")
    second_id = get_or_create_source_other(conn, "Dietitian handout")
    assert first_id != second_id


def test_get_or_create_source_other_stores_as_given(conn: Connection) -> None:
    """
    Assert that the description is stored exactly as given, not normalized.
    """
    source_id = get_or_create_source_other(conn, "  MEMAW'S recipe Card ")
    row = conn.execute(select(sources).where(sources.c.source_id == source_id)).one()
    assert row.description == "  MEMAW'S recipe Card "
# endregion other tests