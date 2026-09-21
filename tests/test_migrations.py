import warnings

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, inspect, text

from menuet.db import PROJECT_ROOT, create_db_engine
from menuet.schema import metadata


def _describe_schema(engine: Engine) -> dict:
    """Collect a comparable description of every table and index."""
    tables = {}

    with warnings.catch_warnings():
        # Expression-based indexes can't be reflected; they're compared separately below.
        warnings.simplefilter("ignore")
        insp = inspect(engine)

        for table_name in insp.get_table_names():
            if table_name == "alembic_version":
                continue

            columns = []
            for col in insp.get_columns(table_name):
                columns.append((col["name"], str(col["type"]), col["nullable"], col["default"]))
            columns.sort()

            primary_key = insp.get_pk_constraint(table_name)["constrained_columns"]

            foreign_keys = []
            for fk in insp.get_foreign_keys(table_name):
                foreign_keys.append((
                    tuple(fk["constrained_columns"]),
                    fk["referred_table"],
                    tuple(fk["referred_columns"]),
                    fk["options"].get("ondelete"),
                ))
            foreign_keys.sort()

            checks = []
            for check in insp.get_check_constraints(table_name):
                checks.append(check["sqltext"])
            checks.sort()

            tables[table_name] = {
                "columns": columns,
                "primary_key": primary_key,
                "foreign_keys": foreign_keys,
                "checks": checks,
            }

    indexes = {}
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT name, sql FROM sqlite_master WHERE type = 'index' AND sql IS NOT NULL"
        ))
        for name, sql in rows:
            indexes[name] = sql

    return {"tables": tables, "indexes": indexes}


def test_migration_schema_matches_create_all() -> None:
    """Assert that migration schema matches created database."""
    migrated = create_db_engine("sqlite://")
    alembic_cfg = Config(
        file_=PROJECT_ROOT / "alembic.ini",
        toml_file=PROJECT_ROOT / "pyproject.toml",
        attributes={"engine": migrated},
    )
    command.upgrade(alembic_cfg, "head")

    expected = create_db_engine("sqlite://")
    metadata.create_all(expected)

    assert _describe_schema(migrated) == _describe_schema(expected)

    migrated.dispose()
    expected.dispose()

