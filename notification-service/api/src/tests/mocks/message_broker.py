from services.message_broker import BaseMessageBroker


class MockMessageBroker(BaseMessageBroker):
    def __init__(self):
        self.messages: list = []

    async def send(self, data):
        self.messages.append(data)
