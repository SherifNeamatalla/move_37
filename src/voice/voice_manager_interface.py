from abc import ABC, abstractmethod
from typing import TypeVar, Optional

T = TypeVar('T')


class IVoiceManager(ABC):
    @abstractmethod
    def say(self, text: str, voice_id: Optional[str] = None) -> T:
        """Say a text"""
        pass
