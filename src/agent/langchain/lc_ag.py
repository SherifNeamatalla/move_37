from langchain import PromptTemplate
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from src.config.constants import DEFAULT_MODEL
from src.prompts.prompt_loader import load_prompt_template
from src.tools.langchain_tools.langchain_tool_index import langchain_tools_list

LANGCHAIN_SINGLE_AGENT_TEMPLATE_NAME = "langchain_single_use_template.txt"


class LCAgent:
    def __init__(self, name, role, model_name=DEFAULT_MODEL, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, temperature=0,
                 max_tokens=4096, verbose=False, output_parser=None):
        self.name = name
        self.role = role

        llm = ChatOpenAI(model_name=model_name, temperature=temperature)

        self.tools = langchain_tools_list()

        self.agent = initialize_agent(self.tools, llm, agent=agent, verbose=verbose)

        response_schemas = [
            ResponseSchema(name="name", description="Name of tool to use"),
            ResponseSchema(name="args", description="Args of tool, separated by ,"),
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


        self.prompt = PromptTemplate(
            template=load_prompt_template(LANGCHAIN_SINGLE_AGENT_TEMPLATE_NAME),
            input_variables=[
                "name",
                "role",
                "tools",
                "format_instructions",
            ]
        ).partial(
            format_instructions=output_parser.get_format_instructions(),
            name=self.name,
            role=self.role,
            tools="\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
        )

    def run(self, prompt):
        return self.agent.run(self.prompt.format())
