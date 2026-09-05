import pytest
from menuet.db import create_db_engine
from menuet.schema import metadata

@pytest.fixture
def conn():
    engine = create_db_engine("sqlite://")
    metadata.create_all(engine)
    with engine.connect() as c:
        yield c