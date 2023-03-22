from asyncio import get_event_loop_policy

import pytest
from config import Config
from httpx import AsyncClient
from main import create_app

from persistency.connection import get_db
from persistency.connection_for_test_db import drop_db, get_test_db

MARKER = """
unit: Mark unit tests
integration: Mark integration tests
high: High Priority
medium: Medium Priority
low: Low Priority
"""


def drop_database(fn):
    async def _reset_db(client_with_db):
        Config.production_mode = False
        await drop_db()
        result = await fn(client_with_db)
        return result

    return _reset_db


@pytest.fixture(scope="session")
def client_with_db():
    Config.production_mode = False
    app = create_app()
    app.dependency_overrides[get_db] = get_test_db
    yield AsyncClient(app=app, base_url="http://tests")
    Config.production_mode = True


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


@pytest.fixture(scope="session")
def event_loop():
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
