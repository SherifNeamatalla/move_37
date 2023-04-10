from abc import ABC, abstractmethod


class IRunner(ABC):

    @abstractmethod
    def run(self):
        """Run the application"""
        pass
