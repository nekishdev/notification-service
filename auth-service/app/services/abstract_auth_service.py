from abc import ABC, abstractmethod


class AbstractAuthService(ABC):
    def __init__(self):
        self.user_data = {}

    @abstractmethod
    def get_auth_link(self):
        pass

    @abstractmethod
    def get_token(self):
        pass

    @abstractmethod
    def get_profile(self):
        pass
