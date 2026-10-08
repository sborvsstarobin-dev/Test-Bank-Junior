import pytest
from src.main.api.db.engine import engine, Session_local

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session_local(bind = connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()