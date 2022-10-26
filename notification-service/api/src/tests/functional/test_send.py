from starlette.testclient import TestClient

from tests.mocks.message_broker import MockMessageBroker


def test_success_sent_to_message_broker(
    app_client: TestClient, message_broker: MockMessageBroker
):
    data = {"address": "test@mail.ru", "source": "email", "text": "hello"}
    response = app_client.post("/api/v1/notify/send", json=data)
    assert response.status_code == 200
    assert len(message_broker.messages) == 1


def test_validation_errors(app_client: TestClient):
    data = {"address": "test@mail.ru"}
    response = app_client.post("/api/v1/notify/send", json=data)
    assert response.status_code == 422

    data = {}
    response = app_client.post("/api/v1/notify/send", json=data)
    assert response.status_code == 422

    response = app_client.post("/api/v1/notify/send")
    assert response.status_code == 422
