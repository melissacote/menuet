from sqlalchemy import Connection, func, insert, select

from menuet.schema import sources


def get_or_create_source_url(conn: Connection, url: str) -> int:
    """Insert a URL source if new and return source_id for new or existing.

    Does not commit; the caller commits.
    """

    # Check for existing source and return if found
    check_stmt = select(sources.c.source_id).where(func.lower(func.trim(sources.c.url)) == func.lower(func.trim(url)))
    existing = conn.execute(check_stmt).scalar_one_or_none()
    if existing is not None:
        return existing

    # Add new source if does not exist
    add_stmt = insert(sources).values(source_type="url", url=url)
    result = conn.execute(add_stmt)
    return result.inserted_primary_key[0]
