-- FK enforcement requires PRAGMA foreign_keys = ON per connection

-- *** RECIPE LIBRARY ***
CREATE TABLE Recipes(
    recipe_id INTEGER PRIMARY KEY,
    recipe_name TEXT NOT NULL,
    like_rating INTEGER CHECK (like_rating BETWEEN 1 AND 5),
    effort_rating INTEGER CHECK (effort_rating BETWEEN 1 AND 5),
    weather TEXT CHECK (weather IN ('warm', 'cool')),
    source TEXT NOT NULL,
    ever_cooked INTEGER NOT NULL DEFAULT 0 CHECK (ever_cooked IN (0, 1)),
    is_included INTEGER NOT NULL DEFAULT 1 CHECK (is_included IN (0, 1))
) STRICT;

-- Checks for uniqueness of recipe names by indexing names in lowercase with trimmed whitespace
CREATE UNIQUE INDEX idx_recipe_name_unique ON Recipes (lower(trim(recipe_name)));

CREATE TABLE Tags(
    tag_id INTEGER PRIMARY KEY,
    tag_name TEXT NOT NULL,
    tag_category TEXT NOT NULL CHECK (tag_category IN
                 ('cuisine', 'style', 'starch', 'protein', 'appliance'))
) STRICT;

-- Checks for uniqueness of tag name and category combinations (names in lowercase with trimmed whitespace)
CREATE UNIQUE INDEX idx_tag_name_category_unique ON Tags (lower(trim(tag_name)), tag_category);

CREATE TABLE RecipeTags(
    recipe_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
                       ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
                       ON DELETE CASCADE
) STRICT;

-- *** MENU PLANNING ***
CREATE TABLE PreferenceSets(
    pref_set_id INTEGER PRIMARY KEY,
    set_name TEXT NOT NULL,
    is_default INTEGER NOT NULL DEFAULT 0 CHECK (is_default IN (0, 1)),
    min_like_rating INTEGER CHECK (min_like_rating BETWEEN 1 AND 5),
    max_effort_rating INTEGER CHECK (max_effort_rating BETWEEN 1 AND 5),
    weather_filter TEXT CHECK (weather_filter IN ('cool', 'warm'))
) STRICT;

-- Checks for uniqueness of set names (lowercase trimmed)
CREATE UNIQUE INDEX idx_set_name_unique ON PreferenceSets (lower(trim(set_name)));

CREATE TABLE Menus(
    menu_id INTEGER PRIMARY KEY,
    pref_set_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pref_set_id) REFERENCES PreferenceSets(pref_set_id)
                  ON DELETE SET NULL
) STRICT;

CREATE TABLE MenuItems(
    menu_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    was_cooked INTEGER DEFAULT 0 NOT NULL CHECK (was_cooked IN (0, 1)),
    PRIMARY KEY (menu_id, recipe_id),
    FOREIGN KEY (menu_id) REFERENCES Menus(menu_id)
                      ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
) STRICT;

CREATE TABLE CategoryLimits(
    pref_set_id INTEGER NOT NULL,
    tag_category TEXT NOT NULL CHECK (tag_category IN
                                      ('cuisine', 'style', 'starch', 'protein', 'appliance')),
    max_count INTEGER NOT NULL CHECK (max_count >= 0),
    PRIMARY KEY (pref_set_id, tag_category),
    FOREIGN KEY (pref_set_id) REFERENCES PreferenceSets(pref_set_id)
                           ON DELETE CASCADE
) STRICT;

CREATE TABLE TagLimits(
    pref_set_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    max_count INTEGER NOT NULL CHECK (max_count >= 0),
    PRIMARY KEY (pref_set_id, tag_id),
    FOREIGN KEY (pref_set_id) REFERENCES PreferenceSets(pref_set_id)
                      ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
                      ON DELETE CASCADE
) STRICT;


