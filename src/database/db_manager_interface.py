from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar('T')


class IDBManager(ABC):
    @abstractmethod
    def add(self, data: str) -> T:
        """Add a new row to the database"""
        pass

    @abstractmethod
    def delete(self, row_id: str) -> T:
        """Delete a row from the database"""
        pass

    @abstractmethod
    def update(self, row_id: str, data: any) -> T:
        """Update a row in the database"""
        pass

    @abstractmethod
    def get(self, row_id: str) -> T:
        """Get a row from the database"""
        pass

    @abstractmethod
    def list(self) -> [T]:
        """List all rows in the database"""
        pass
