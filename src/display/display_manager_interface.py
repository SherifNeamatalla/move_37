from abc import ABC, abstractmethod


class IDisplayManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def print(self, text: str):
        pass

    @abstractmethod
    def prompt(self, text: str):
        pass
