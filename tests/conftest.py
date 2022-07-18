from typing import Generator

import pytest
from flask import Flask


@pytest.fixture()
def app() -> Flask:
    """Fixture that creates app for testing"""
    import dhos_notifications_api.app

    return dhos_notifications_api.app.create_app(testing=True)


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield
