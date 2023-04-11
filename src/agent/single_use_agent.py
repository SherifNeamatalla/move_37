from typing import Optional

import openai
from langchain import PromptTemplate

from src.agent.agent_config import AgentConfig
from src.config.constants import DEFAULT_MODEL
from src.util.messages_util import create_system_message
from src.util.token_util import create_chat_bot_context


class SingleUserAgent:
    def __init__(self, prompt_template: PromptTemplate, user_input_template: Optional[PromptTemplate] = None):
        self.prompt = prompt_template
        self.user_input_template = user_input_template
        self.config = AgentConfig(
            model=DEFAULT_MODEL,
            temperature=0,
            max_tokens=4096
        )

    def chat(self, user_input: Optional[str] = None, prompt_input: Optional[dict] = None) -> str:
        """Chat with the agent, this is the main method of the agent"""

        # This creates relevant context based on user input, this will fetch the relevant context from the short term
        # memory , long term memory and the prompt
        context, remaining_tokens = self.create_context(user_input, prompt_input)

        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        agent_response = response.choices[0].message["content"]

        return agent_response

    def create_context(self, user_input: str, prompt_input: dict) -> (str, int):
        if not prompt_input:
            prompt_input = {}
        context = [create_system_message(self.prompt.format(**prompt_input))]

        user_input_full_prompt = user_input

        if self.user_input_template:
            user_input_full_prompt = self.user_input_template.format(user_input=user_input)

        return create_chat_bot_context(
            model=self.config.get('model'),
            max_tokens=self.config.get('max_tokens'),
            user_input=user_input_full_prompt,
            full_message_history=[],
            context=context
        )
