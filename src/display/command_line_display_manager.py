from src.display.display_manager_interface import IDisplayManager


class CommandLineDisplayManager(IDisplayManager):

    def print(self, text: str):
        print(text)

    def prompt(self, text: str):
        return input(text)
