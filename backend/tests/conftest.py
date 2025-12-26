import pytest
from quart import Quart

from backend.run import app, db


@pytest.fixture(name="app")
async def _app():
    async with app.test_app():
        yield app


@pytest.fixture(name="connection")
async def _connection(app: Quart):
    async with db.connection() as connection:
        async with connection.transaction():
            yield connection
