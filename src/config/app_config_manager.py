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
        # TODO(3amr) db
        pass

    def load(self, agent_id):
        # TODO(3amr) db
        pass

    def list(self):
        # TODO(3amr) db
        pass
