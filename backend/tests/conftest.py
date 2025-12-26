import pytest
import pytest_asyncio
from quart import Quart

from backend.run import app, db


@pytest.fixture(name="app")
async def _app():
    async with app.test_app():
        yield app


@pytest_asyncio.fixture(name="connection", scope="function")
async def _connection(app: Quart):
    async with db.connection() as connection:
        async with connection.transaction():
            yield connection
