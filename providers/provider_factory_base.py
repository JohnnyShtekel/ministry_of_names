from abc import ABC, abstractmethod


class ProviderFactoryBase(ABC):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @abstractmethod
    def create(self):
        pass