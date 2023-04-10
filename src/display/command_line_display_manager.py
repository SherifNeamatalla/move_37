from typing import Optional

from src.display.display_manager_interface import IDisplayManager


class CommandLineDisplayManager(IDisplayManager):

    def print(self, text: str):
        print(text)

    def prompt(self, text: str, tool_name: Optional[str] = None):
        if tool_name:
            text = f"Permission to use {tool_name}: {text}, y/n? (Text for human feedback)"
        return input(text)
