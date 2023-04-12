import os

import yaml

from src.config.constants import AGENTS_DIR
from src.database.db_manager_interface import IDBManager
from src.display.display_manager_interface import IDisplayManager
from src.voice.voice_manager_interface import IVoiceManager


class AppConfigManager:
    _instance = None

    def __new__(cls, voice_manager: IVoiceManager = None, db_manager: IDBManager = None,
                display_manager: IDisplayManager = None):
        if cls._instance is None:
            cls.voice_manager = voice_manager
            cls.db_manager = db_manager
            cls.display_manager = display_manager
            cls._instance = super().__new__(cls)
        return cls._instance

    def display(self, text: str):
        if not self.display_manager:
            return
        self.display_manager.print(text)

    def prompt(self, text: str):
        if not self.display_manager:
            return
        return self.display_manager.prompt(text)

    def voice(self, text: str):
        self.voice_manager.say(text)

    def save(self, agent):
        directory = os.path.join(AGENTS_DIR, agent.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, 'config.yaml'), 'w') as f:
            yaml.dump(agent.to_dict(), f)

    def load(self, agent_id: str):
        directory = os.path.join(AGENTS_DIR, agent_id)

        if not os.path.exists(directory):
            return None

        with open(os.path.join(directory, 'config.yaml'), 'r') as f:
            agent_dict = yaml.load(f, Loader=yaml.FullLoader)

        return agent_dict

    def list(self) -> [str]:
        directory = os.path.join(AGENTS_DIR)

        if not os.path.exists(directory):
            return []

        return os.listdir(directory)
