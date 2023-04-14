# Set up a prompt template
from typing import List, Any

from langchain.agents import Tool
from langchain.prompts import BaseChatPromptTemplate
from langchain.schema import HumanMessage

from src.prompts.prompt_loader import load_prompt_template


class LCSingleUseAGTemplate(BaseChatPromptTemplate):
    # The list of tools available
    tools: List[Tool]

    def __init__(self, name, role, **data: Any):
        from src.agent.langchain.lc_ag import LANGCHAIN_SINGLE_AGENT_TEMPLATE_NAME
        # Set the template
        super().__init__(**data)
        self.name = name
        self.role = role
        self.template = load_prompt_template(LANGCHAIN_SINGLE_AGENT_TEMPLATE_NAME)

    def format_messages(self, **kwargs) -> List[HumanMessage]:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        # Add app custom variables
        kwargs["name"] = self.name
        kwargs["role"] = self.role
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]
