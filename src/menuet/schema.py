from sqlalchemy import MetaData, Table, Column, Integer, Text, CheckConstraint, ForeignKey, Index, func, text

metadata = MetaData()

# *** RECIPE LIBRARY ***
sources = Table(
    'Sources', metadata,
    Column('source_id', Integer, primary_key=True),
    Column('source_type', Text,
           CheckConstraint("source_type IN ('url', 'book', 'other')",
                           name='ck_sources_source_type'),
           nullable=False),
    Column('url', Text),
    Column('book_title', Text),
    Column('book_author', Text),
    Column('description', Text), # description is used for other type
    CheckConstraint(
        "(source_type = 'url' AND url IS NOT NULL "
        "AND book_title IS NULL AND book_author IS NULL "
        "AND description IS NULL) OR "
        "(source_type = 'book' AND book_title IS NOT NULL AND book_author IS NOT NULL "
        "AND url IS NULL AND description IS NULL) OR "
        "(source_type = 'other' AND description IS NOT NULL "
        "AND url IS NULL AND book_title IS NULL "
        "AND book_author IS NULL)",
        name='ck_source_type_fields'
    ),
    sqlite_strict=True
)

Index(
    'idx_source_url_unique',
    func.lower(func.trim(sources.c.url)),
    unique=True,
)

Index(
    'idx_source_book_unique',
    func.lower(func.trim(sources.c.book_title)),
    func.lower(func.trim(sources.c.book_author)),
    unique=True,
)

Index(
    'idx_source_description_unique',
    func.lower(func.trim(sources.c.description)),
    unique=True,
)

recipes = Table(
    'Recipes', metadata,
    Column('recipe_id', Integer, primary_key=True),
    Column('recipe_name', Text, nullable=False),
    Column('like_rating', Integer,
           CheckConstraint('like_rating BETWEEN 1 AND 5',
                           name='ck_recipes_like_rating')),
    Column('effort_rating', Integer,
           CheckConstraint('effort_rating BETWEEN 1 AND 5',
                           name='ck_recipes_effort_rating')),
    Column('weather', Text,
           CheckConstraint("weather IN ('warm', 'cool')",
                           name='ck_recipes_weather')),
    Column('source_id', Integer,
           ForeignKey("Sources.source_id",),
           nullable=False),
    Column('ever_cooked', Integer,
           CheckConstraint("ever_cooked IN (0, 1)",
                           name='ck_recipes_ever_cooked'),
           nullable=False, server_default=text('0')),
    Column('is_included', Integer,
           CheckConstraint('is_included IN (0, 1)',
                           name='ck_recipes_is_included'),
           nullable=False, server_default=text('1')),
    sqlite_strict=True
)

Index(
    'idx_recipe_name_unique',
    func.lower(func.trim(recipes.c.recipe_name)),
    unique=True
)

tags = Table(
    'Tags', metadata,
    Column('tag_id', Integer, primary_key=True),
    Column('tag_name', Text, nullable=False),
    Column('tag_category', Text,
           CheckConstraint(
               "tag_category IN "
               "('cuisine', 'style', 'starch', 'protein', 'appliance')",
               name='ck_tags_tag_category'
           ),
           nullable=False),
    sqlite_strict=True
)

Index(
    'idx_tag_name_category_unique',
    func.lower(func.trim(tags.c.tag_name)),
    tags.c.tag_category,
    unique=True
)

recipe_tags = Table(
    'RecipeTags', metadata,
    Column('recipe_id', Integer,
           ForeignKey("Recipes.recipe_id", ondelete="CASCADE"),
           nullable=False, primary_key=True),
    Column('tag_id', Integer,
           ForeignKey("Tags.tag_id", ondelete="CASCADE"),
           nullable=False, primary_key=True),
    sqlite_strict=True
)

# *** MENU PLANNING ***
preference_sets = Table(
    'PreferenceSets', metadata,
    Column('pref_set_id', Integer, primary_key=True),
    Column('set_name', Text, nullable=False),
    Column('is_default', Integer,
           CheckConstraint('is_default IN (0, 1)',
                           name='ck_preferencesets_is_default'),
           nullable=False, server_default=text('0')),
    Column('min_like_rating', Integer,
           CheckConstraint('min_like_rating BETWEEN 1 AND 5',
                           name='ck_preferencesets_min_like_rating')),
    Column('max_effort_rating', Integer,
           CheckConstraint('max_effort_rating BETWEEN 1 AND 5',
                           name='ck_preferencesets_max_effort_rating')),
    Column('weather_filter', Text,
           CheckConstraint("weather_filter IN ('warm', 'cool')",
                           name='ck_preferencesets_weather_filter')),
    sqlite_strict=True
)

Index(
    'idx_set_name_unique',
    func.lower(func.trim(preference_sets.c.set_name)),
    unique=True
)

menus = Table(
    'Menus', metadata,
    Column('menu_id', Integer, primary_key=True),
    Column('pref_set_id', Integer,
           ForeignKey("PreferenceSets.pref_set_id", ondelete="SET NULL")),
    Column('created_at', Text,
           nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    sqlite_strict=True
)

menu_items = Table(
    'MenuItems', metadata,
    Column('menu_id', Integer,
           ForeignKey("Menus.menu_id", ondelete="CASCADE"),
           nullable=False, primary_key=True),
    Column('recipe_id', Integer,
           ForeignKey("Recipes.recipe_id"),
           nullable=False, primary_key=True),
    Column('was_cooked', Integer,
           CheckConstraint('was_cooked IN (0, 1)',
                           name='ck_menuitems_was_cooked'),
           nullable=False, server_default=text('0')),
    sqlite_strict=True
)

category_limits = Table(
    'CategoryLimits', metadata,
    Column('pref_set_id', Integer,
           ForeignKey("PreferenceSets.pref_set_id", ondelete="CASCADE"),
           nullable=False, primary_key=True),
    Column('tag_category', Text,
           CheckConstraint("tag_category IN ('cuisine', 'style', 'starch', 'protein', 'appliance')",
                           name='ck_categorylimits_tag_category'),
           nullable=False, primary_key=True),
    Column('max_count', Integer,
           CheckConstraint('max_count >= 0',
                           name='ck_categorylimits_max_count'),
           nullable=False),
    sqlite_strict=True
)

tag_limits = Table(
    'TagLimits', metadata,
    Column('pref_set_id', Integer,
           ForeignKey("PreferenceSets.pref_set_id", ondelete="CASCADE"),
           nullable=False, primary_key=True),
    Column('tag_id', Integer,
           ForeignKey("Tags.tag_id", ondelete="CASCADE"),
           nullable=False, primary_key=True),
    Column('max_count', Integer,
           CheckConstraint('max_count >= 0',
                           name='ck_taglimits_max_count'),
           nullable=False),
    sqlite_strict=True
)






