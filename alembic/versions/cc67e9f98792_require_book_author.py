"""require book author

Revision ID: cc67e9f98792
Revises: b7d0bf092510
Create Date: 2026-11-07 23:57:37.302195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

NEW_CHECK = ("(source_type = 'url' AND url IS NOT NULL "
                "AND book_title IS NULL AND book_author IS NULL "
                "AND description IS NULL) OR "
                "(source_type = 'book' AND book_title IS NOT NULL AND book_author IS NOT NULL "
                "AND url IS NULL AND description IS NULL) OR "
                "(source_type = 'other' AND description IS NOT NULL "
                "AND url IS NULL AND book_title IS NULL "
                "AND book_author IS NULL)")

OLD_CHECK = ("(source_type = 'url' AND url IS NOT NULL "
                "AND book_title IS NULL AND book_author IS NULL "
                "AND description IS NULL) OR "
                "(source_type = 'book' AND book_title IS NOT NULL "
                "AND url IS NULL AND description IS NULL) OR "
                "(source_type = 'other' AND description IS NOT NULL "
                "AND url IS NULL AND book_title IS NULL "
                "AND book_author IS NULL)")

def _create_source_indexes() -> None:
    op.create_index(
        'idx_source_url_unique',
        'Sources',
        [sa.text('lower(trim(url))')],
        unique=True,
    )
    op.create_index(
        'idx_source_book_unique',
        'Sources',
        [sa.text('lower(trim(book_title))'), sa.text('lower(trim(book_author))')],
        unique=True,
    )
    op.create_index(
        'idx_source_description_unique',
        'Sources',
        [sa.text('lower(trim(description))')],
        unique=True,
    )


# revision identifiers, used by Alembic.
revision: str = 'cc67e9f98792'
down_revision: Union[str, Sequence[str], None] = 'b7d0bf092510'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('Sources') as batch_op:
        batch_op.drop_constraint('ck_source_type_fields', type_='check')
        batch_op.create_check_constraint('ck_source_type_fields', NEW_CHECK)
    _create_source_indexes()


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('Sources') as batch_op:
        batch_op.drop_constraint('ck_source_type_fields', type_='check')
        batch_op.create_check_constraint('ck_source_type_fields', OLD_CHECK)
    _create_source_indexes()
