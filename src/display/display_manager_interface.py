from abc import ABC, abstractmethod
from typing import Optional


class IDisplayManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def print(self, text: str):
        pass

    @abstractmethod
    def prompt(self, text: str, tool_name: Optional[str] = None):
        pass
