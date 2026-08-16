import pytest
from src.db import get_connection

@pytest.fixture
def conn():
    with get_connection(":memory:") as c:
        yield c