from typing import Optional

from src.config.constants import USER_ROLE, ASSISTANT_ROLE, SYSTEM_ROLE
from src.util.messages_util import create_user_message, create_agent_message, create_system_message


class AgentMemory:

    def __init__(self, chat_history: [] = None):
        self.chat_history = chat_history or []

    def __dict__(self):
        return {
            "chat_history": self.chat_history
        }

    def add_user_input(self, user_input: str):
        self.chat_history.append(create_user_message(user_input))

    def add_agent_input(self, agent_input: str):
        self.chat_history.append(create_agent_message(agent_input))

    def add_system_input(self, system_input: str):
        self.chat_history.append(create_system_message(system_input))

    def get_last_message(self, role: Optional[str] = None) -> Optional[str]:
        if not role:
            return self.chat_history[-1]

        for message in reversed(self.chat_history):
            if message['role'] == role:
                return message['content']

    def get_last_user_message(self) -> Optional[str]:
        return self.get_last_message(USER_ROLE)

    def get_last_agent_message(self) -> Optional[str]:
        return self.get_last_message(ASSISTANT_ROLE)

    def get_last_system_message(self) -> Optional[str]:
        return self.get_last_message(SYSTEM_ROLE)

    def add_tool_error(self, error: any):
        tool_memory_entry = f"Command failed, error:{str(error)}"

        self.chat_history.append(create_system_message(tool_memory_entry))

    def add_tool_result(self, tool_name: str, tool_result: Optional[str] = 'None'):
        if not tool_result:
            tool_memory_entry = f"Unable to execute tool {tool_name}"
        else:
            tool_memory_entry = f"Command {tool_name} returned: {tool_result}, save important information in " \
                                f"memory!"

        self.chat_history.append(create_system_message(tool_memory_entry))

    def add_human_feedback(self, user_input: str):
        result = f"Human feedback: {user_input}"
        self.chat_history.append(create_user_message(result))

    def save(self):
        """This method will save the memory to the database"""
        messages = []

        for message in self.chat_history:
            messages.append(f"{message['role']}: {message['content']}")
