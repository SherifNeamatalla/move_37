from langchain import PromptTemplate

from langchain import PromptTemplate

from src.agent.agent import Agent
from src.config.constants import DEFAULT_USER_INPUT_TEMPLATE
from src.prompts.prompt_loader import load_prompt_template, load_toolset
from src.util.messages_util import create_system_message
from src.util.token_util import create_chat_bot_context


class SingleFunctionAgent(Agent):
    def create_context(self, user_input: str) -> (str, int):
        context = [create_system_message(self.prompt.format(
            name=self.name,
            role=self.role,
            goals=self.goals,
            tools=self.config.get('toolset_name')
        ))]

        user_input_full_prompt = PromptTemplate(
            input_variables=['user_input'],
            template=load_prompt_template(DEFAULT_USER_INPUT_TEMPLATE)
        ).format(user_input=user_input)

        return create_chat_bot_context(
            model=self.config.get('model'),
            max_tokens=self.config.get('max_tokens'),
            user_input=user_input_full_prompt,
            full_message_history=self.memory.chat_history,
            context=context
        )
