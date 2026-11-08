from sqlalchemy import Connection, func, insert, select

from menuet.schema import sources


def get_or_create_source_url(conn: Connection, url: str) -> int:
    """Insert a URL source if new and return source_id for new or existing.

    Does not commit; the caller commits.
    """

    # Check for existing source and return if found
    check_stmt = select(sources.c.source_id).where(
        func.lower(func.trim(sources.c.url)) == func.lower(func.trim(url)))
    existing = conn.execute(check_stmt).scalar_one_or_none()
    if existing is not None:
        return existing

    # Add new source if it does not exist
    add_stmt = insert(sources).values(source_type="url", url=url)
    result = conn.execute(add_stmt)
    return result.inserted_primary_key[0]

def get_or_create_source_book(conn: Connection, book_title: str, book_author: str) -> int:
    """Insert a book source if new and return source_id for new or existing.

    Does not commit; the caller commits.
    """

    # Check for existing source and return if found
    check_stmt = select(sources.c.source_id).where(
        func.lower(func.trim(sources.c.book_title)) == func.lower(func.trim(book_title)),
        func.lower(func.trim(sources.c.book_author)) == func.lower(func.trim(book_author)),
    )
    existing = conn.execute(check_stmt).scalar_one_or_none()
    if existing is not None:
        return existing

    # Add new source if it does not exist
    add_stmt = insert(sources).values(source_type="book", book_title=book_title, book_author=book_author)
    result = conn.execute(add_stmt)
    return result.inserted_primary_key[0]

def get_or_create_source_other(conn: Connection, description: str) -> int:
    """Insert a source (other type) if new and return source_id for new or existing.

    Does not commit; the caller commits.
    """

    # Check for existing source and return if found
    check_stmt = select(sources.c.source_id).where(
        func.lower(func.trim(sources.c.description)) == func.lower(func.trim(description))
    )
    existing = conn.execute(check_stmt).scalar_one_or_none()
    if existing is not None:
        return existing

    # Add new source if it does not exist
    add_stmt = insert(sources).values(source_type="other", description=description)
    result = conn.execute(add_stmt)
    return result.inserted_primary_key[0]





