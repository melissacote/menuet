import pytest
from sqlalchemy import Connection, text, insert, select
from sqlalchemy.exc import IntegrityError

from menuet.schema import recipes, tags


def test_db_fk(conn: Connection) -> None:
    """Assert that foreign key enforcement is on."""
    result = conn.execute(text("PRAGMA foreign_keys")).fetchone()
    assert result[0] == 1

def test_insert_recipe(conn: Connection) -> None:
    """Assert that a recipe can be inserted and expected values (including defaults) returned."""
    conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source='book'))
    row = conn.execute(select(recipes)).fetchone()
    assert row.recipe_name == 'test'
    assert row.like_rating == 3
    assert row.source == 'book'
    assert row.ever_cooked == 0
    assert row.is_included == 1

def test_check_constraint_fail(conn: Connection) -> None:
    """Assert that check constraint rejects invalid input."""
    with pytest.raises(IntegrityError):
        conn.execute(insert(recipes).values(recipe_name='test', like_rating=10, source='book'))

def test_unique_index_allows_distinct_names(conn: Connection) -> None:
    """Assert that unique index accepts distinct values."""
    conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source='book'))
    conn.execute(insert(recipes).values(recipe_name='test2', like_rating=3, source='book'))

def test_unique_index_case(conn: Connection) -> None:
    """Assert that unique index rejects values based on case."""
    conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source='book'))
    with pytest.raises(IntegrityError):
        conn.execute(insert(recipes).values(recipe_name='Test', like_rating=3, source='book'))

def test_unique_index_whitespace(conn: Connection) -> None:
    """Assert that unique index rejects values based on whitespace."""
    conn.execute(insert(tags).values(tag_name='test', tag_category='cuisine'))
    with pytest.raises(IntegrityError):
        conn.execute(insert(tags).values(tag_name=' test ', tag_category='cuisine'))



