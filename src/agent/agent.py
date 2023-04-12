import json
import uuid
from typing import Optional

import openai
from langchain import PromptTemplate

from src.agent.agent_config import AgentConfig
from src.agent.memory.agent_memory import AgentMemory
from src.agent.memory.pinecone_agent_memory import PineconeAgentMemory
from src.agent.prompts.base_prompt_template import AppBasePromptTemplate
from src.config.constants import DEFAULT_EMPTY_USER_INPUT_TEMPLATE_NAME, DEFAULT_USER_INPUT_TEMPLATE
from src.prompts.prompt_loader import load_prompt_template, load_toolset
from src.util.messages_util import create_system_message
from src.util.token_util import create_chat_bot_context


class Agent:
    """This agent uses Pinecone as a longterm memory solution"""

    def __init__(self, name: str, role: str, config: AgentConfig, goals: [] = None,
                 memory: AgentMemory = None, agent_id: Optional[str] = None):
        if not goals:
            goals = []

        if not memory:
            memory = AgentMemory()

        self.id = agent_id if agent_id else uuid.uuid4()
        self.name = name
        self.role = role
        self.goals = goals
        self.config = config
        self.memory = memory
        self.personal_goals = []
        self.summary = ' '
        self.prompt = AppBasePromptTemplate()
        self.long_term_memory = PineconeAgentMemory(self.id)

    def to_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name,
            'role': self.role,
            'goals': self.goals,
            'config': self.config.to_dict(),
        }

    def chat(self, user_input: Optional[str] = None) -> str:
        """Chat with the agent, this is the main method of the agent"""
        """This method will be called by the runner as a part of the chat loop"""

        original_user_input = user_input

        if not user_input:
            user_input = load_prompt_template(DEFAULT_EMPTY_USER_INPUT_TEMPLATE_NAME)

        # This creates relevant context based on user input, this will fetch the relevant context from the short term
        # memory , long term memory and the prompt
        context, remaining_tokens = self.create_context(user_input)

        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        agent_response = response.choices[0].message["content"]

        if original_user_input:
            self.memory.add_user_input(original_user_input)

        self.memory.add_agent_input(agent_response)

        try:
            response = json.loads(agent_response)

            self.personal_goals = response['thoughts']["goals"].split("\n")
            self.summary = response['thoughts']["summary"]

            if 'save_to_memory' in response['thoughts'] and response['thoughts']['save_to_memory'] is not None:
                self.long_term_memory.add_to_memory(response['thoughts']['save_to_memory'])
        except:
            pass

        return agent_response

    def create_context(self, user_input: str) -> (str, int):
        relevant_messages = self.long_term_memory.get_relevant_memory(self.summary)

        relevant_messages = '\n'.join(relevant_messages)

        context = [create_system_message(self.prompt.format(
            name=self.name,
            role=self.role,
            goals=self.goals,
            tools=load_toolset(self.config.get('toolset_name')),
            user_goals='\n'.join(self.goals),
            personal_goals='\n'.join(self.personal_goals),
            summary=self.summary,
            context=relevant_messages
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

    @staticmethod
    def load_from_dict(data: dict) -> 'Agent':
        agent_id = data.get('id')
        name = data.get('name')
        role = data.get('role')
        config = AgentConfig.from_dict(data.get('config'))
        goals = data.get('goals')
        memory = data.get('memory', None)

        return Agent(
            name=name,
            role=role,
            config=config,
            agent_id=agent_id,
            goals=goals,
            memory=memory
        )
