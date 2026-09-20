import pytest
from sqlalchemy import Connection, text, insert, select, delete
from sqlalchemy.exc import IntegrityError

from menuet.schema import recipes, tags, sources, recipe_tags


def test_db_fk(conn: Connection) -> None:
    """Assert that foreign key enforcement is on."""
    result = conn.execute(text("PRAGMA foreign_keys")).fetchone()
    assert result[0] == 1

def test_insert_recipe(conn: Connection) -> None:
    """Assert that a recipe can be inserted and expected values (including defaults) returned."""
    source = conn.execute(insert(sources).values(source_type='book', book_title='test_book'))
    source_id = source.inserted_primary_key[0]

    conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source_id=source_id))
    row = conn.execute(select(recipes)).fetchone()

    assert row.recipe_name == 'test'
    assert row.like_rating == 3
    assert row.source_id == source_id
    assert row.ever_cooked == 0
    assert row.is_included == 1

def test_check_constraint_fail(conn: Connection) -> None:
    """Assert that check constraint rejects invalid input."""
    source = conn.execute(insert(sources).values(source_type='book', book_title='test_book'))
    source_id = source.inserted_primary_key[0]

    with pytest.raises(IntegrityError):
        conn.execute(insert(recipes).values(recipe_name='test', like_rating=10, source_id=source_id))

def test_unique_index_allows_distinct_names(conn: Connection) -> None:
    """Assert that unique index accepts distinct values."""
    source = conn.execute(insert(sources).values(source_type='book', book_title='test_book'))
    source_id = source.inserted_primary_key[0]

    conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source_id=source_id))
    conn.execute(insert(recipes).values(recipe_name='test2', like_rating=3, source_id=source_id))

def test_unique_index_case(conn: Connection) -> None:
    """Assert that unique index rejects values based on case."""
    source = conn.execute(insert(sources).values(source_type='book', book_title='test_book'))
    source_id = source.inserted_primary_key[0]

    conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source_id=source_id))
    with pytest.raises(IntegrityError):
        conn.execute(insert(recipes).values(recipe_name='Test', like_rating=3, source_id=source_id))

def test_unique_index_whitespace(conn: Connection) -> None:
    """Assert that unique index rejects values based on whitespace."""
    conn.execute(insert(tags).values(tag_name='test', tag_category='cuisine'))
    with pytest.raises(IntegrityError):
        conn.execute(insert(tags).values(tag_name=' test ', tag_category='cuisine'))

def test_sources_check_allows(conn: Connection) -> None:
    """Assert that source insert check allows appropriate insertions."""
    conn.execute(insert(sources).values(source_type='book', book_title='test_book'))
    conn.execute(insert(sources).values(source_type='url', url='test_url'))
    conn.execute(insert(sources).values(source_type='other', description='text'))

def test_sources_check_forbids(conn: Connection) -> None:
    """Assert that source insert check forbids inappropriate insertions."""
    with pytest.raises(IntegrityError):
        conn.execute(insert(sources).values(source_type='book', book_title='test_book', url='test_url'))

def test_recipetags_foreignkey_cascade(conn: Connection) -> None:
    """Assert that Recipes row deletion cascades to RecipeTags as expected."""
    source = conn.execute(insert(sources).values(source_type='book', book_title='test_book'))
    source_id = source.inserted_primary_key[0]
    tag = conn.execute(insert(tags).values(tag_name='test', tag_category='cuisine'))
    tag_id = tag.inserted_primary_key[0]
    recipe = conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source_id=source_id))
    recipe_id = recipe.inserted_primary_key[0]

    conn.execute(insert(recipe_tags).values(recipe_id=recipe_id, tag_id=tag_id))
    row = conn.execute(select(recipe_tags)).fetchone()
    assert row is not None

    conn.execute(delete(recipes))
    row = conn.execute(select(recipe_tags)).fetchone()
    assert row is None

def test_sources_delete_restricted(conn: Connection) -> None:
    """Assert that a source referenced by a recipe cannot be deleted."""
    source = conn.execute(insert(sources).values(source_type='book', book_title='test_book'))
    source_id = source.inserted_primary_key[0]
    conn.execute(insert(recipes).values(recipe_name='test', like_rating=3, source_id=source_id))

    with pytest.raises(IntegrityError):
        conn.execute(delete(sources))






