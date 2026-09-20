# Menuet

[![Tests](https://github.com/melissacote/menuet/actions/workflows/tests.yml/badge.svg)](https://github.com/melissacote/menuet/actions/workflows/tests.yml)

> *My name is Minuet, and I love all jazz, except Dixieland.*

Menuet is a personal meal-planning app for storing recipes, tagging them, and building menus within category and tag limits.

**Status:** Early development. The database schema, connection layer, and test suite are in place; a FastAPI web interface is planned.

## Stack

- Python 3.12, SQLite
- SQLAlchemy Core
- Alembic for migrations
- pytest, with GitHub Actions CI

## Getting started

```bash
git clone https://github.com/melissacote/menuet.git
cd menuet
pip install -e ".[dev]"
python -m pytest -v
```
