"""initial schema

Revision ID: b7d0bf092510
Revises: 
Create Date: 2026-09-20 20:38:58.539883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7d0bf092510'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('PreferenceSets',
    sa.Column('pref_set_id', sa.Integer(), nullable=False),
    sa.Column('set_name', sa.Text(), nullable=False),
    sa.Column('is_default', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('min_like_rating', sa.Integer(), nullable=True),
    sa.Column('max_effort_rating', sa.Integer(), nullable=True),
    sa.Column('weather_filter', sa.Text(), nullable=True),
    sa.CheckConstraint('is_default IN (0, 1)'),
    sa.CheckConstraint('min_like_rating BETWEEN 1 AND 5'),
    sa.CheckConstraint('max_effort_rating BETWEEN 1 AND 5'),
    sa.CheckConstraint("weather_filter IN ('warm', 'cool')"),
    sa.PrimaryKeyConstraint('pref_set_id'),
    sqlite_strict=True
    )
    op.create_table('Sources',
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('source_type', sa.Text(), nullable=False),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('book_title', sa.Text(), nullable=True),
    sa.Column('book_author', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.CheckConstraint("source_type IN ('url', 'book', 'other')"),
    sa.CheckConstraint("(source_type = 'url' AND url IS NOT NULL AND book_title IS NULL AND book_author IS NULL AND description IS NULL) OR (source_type = 'book' AND book_title IS NOT NULL AND url IS NULL AND description IS NULL) OR (source_type = 'other' AND description IS NOT NULL AND url IS NULL AND book_title IS NULL AND book_author IS NULL)", name='ck_source_type_fields'),
    sa.PrimaryKeyConstraint('source_id'),
    sqlite_strict=True
    )
    op.create_table('Tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.Text(), nullable=False),
    sa.Column('tag_category', sa.Text(), nullable=False),
    sa.CheckConstraint("tag_category IN ('cuisine', 'style', 'starch', 'protein', 'appliance')"),
    sa.PrimaryKeyConstraint('tag_id'),
    sqlite_strict=True
    )
    op.create_table('CategoryLimits',
    sa.Column('pref_set_id', sa.Integer(), nullable=False),
    sa.Column('tag_category', sa.Text(), nullable=False),
    sa.Column('max_count', sa.Integer(), nullable=False),
    sa.CheckConstraint("tag_category IN ('cuisine', 'style', 'starch', 'protein', 'appliance')"),
    sa.CheckConstraint('max_count >= 0'),
    sa.ForeignKeyConstraint(['pref_set_id'], ['PreferenceSets.pref_set_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('pref_set_id', 'tag_category'),
    sqlite_strict=True
    )
    op.create_table('Menus',
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('pref_set_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.Text(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['pref_set_id'], ['PreferenceSets.pref_set_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('menu_id'),
    sqlite_strict=True
    )
    op.create_table('Recipes',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('recipe_name', sa.Text(), nullable=False),
    sa.Column('like_rating', sa.Integer(), nullable=True),
    sa.Column('effort_rating', sa.Integer(), nullable=True),
    sa.Column('weather', sa.Text(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('ever_cooked', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('is_included', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.CheckConstraint('like_rating BETWEEN 1 AND 5'),
    sa.CheckConstraint('effort_rating BETWEEN 1 AND 5'),
    sa.CheckConstraint("weather IN ('warm', 'cool')"),
    sa.CheckConstraint('ever_cooked IN (0, 1)'),
    sa.CheckConstraint('is_included IN (0, 1)'),
    sa.ForeignKeyConstraint(['source_id'], ['Sources.source_id'], ),
    sa.PrimaryKeyConstraint('recipe_id'),
    sqlite_strict=True
    )
    op.create_table('TagLimits',
    sa.Column('pref_set_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('max_count', sa.Integer(), nullable=False),
    sa.CheckConstraint('max_count >= 0'),
    sa.ForeignKeyConstraint(['pref_set_id'], ['PreferenceSets.pref_set_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['Tags.tag_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('pref_set_id', 'tag_id'),
    sqlite_strict=True
    )
    op.create_table('MenuItems',
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('was_cooked', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.CheckConstraint('was_cooked IN (0, 1)'),
    sa.ForeignKeyConstraint(['menu_id'], ['Menus.menu_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('menu_id', 'recipe_id'),
    sqlite_strict=True
    )
    op.create_table('RecipeTags',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipes.recipe_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['Tags.tag_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('recipe_id', 'tag_id'),
    sqlite_strict=True
    )

    # Expression-based unique indexes (not picked up by autogenerate)
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
    op.create_index(
        'idx_recipe_name_unique',
        'Recipes',
        [sa.text('lower(trim(recipe_name))')],
        unique=True,
    )
    op.create_index(
        'idx_tag_name_category_unique',
        'Tags',
        [sa.text('lower(trim(tag_name))'), 'tag_category'],
        unique=True,
    )
    op.create_index(
        'idx_set_name_unique',
        'PreferenceSets',
        [sa.text('lower(trim(set_name))')],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_set_name_unique', table_name='PreferenceSets')
    op.drop_index('idx_tag_name_category_unique', table_name='Tags')
    op.drop_index('idx_recipe_name_unique', table_name='Recipes')
    op.drop_index('idx_source_description_unique', table_name='Sources')
    op.drop_index('idx_source_book_unique', table_name='Sources')
    op.drop_index('idx_source_url_unique', table_name='Sources')
    op.drop_table('RecipeTags')
    op.drop_table('MenuItems')
    op.drop_table('TagLimits')
    op.drop_table('Recipes')
    op.drop_table('Menus')
    op.drop_table('CategoryLimits')
    op.drop_table('Tags')
    op.drop_table('Sources')
    op.drop_table('PreferenceSets')