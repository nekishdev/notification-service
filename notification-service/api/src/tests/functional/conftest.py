import pytest
from fastapi.testclient import TestClient

import providers
from app import app
from tests.mocks.message_broker import MockMessageBroker


@pytest.fixture(scope="session")
def message_broker():
    return MockMessageBroker()


@pytest.fixture(scope="session")
def app_client(message_broker):
    app.dependency_overrides[providers.get_message_broker] = lambda: message_broker
    return TestClient(app)
