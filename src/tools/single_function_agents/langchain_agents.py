from langchain import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.chat_models import ChatOpenAI
from langchain.tools import AIPluginTool
from langchain.utilities.zapier import ZapierNLAWrapper

from src.config.env_loader import load_env
from src.tools.tool_annotation import app_tool

load_env()


@app_tool("Klarna Agent")
def klarna_agent(query):
    """Asks a specialised Klarna GPT agent for shopping information"""
    tool = AIPluginTool.from_plugin_url("https://www.klarna.com/.well-known/ai-plugin.json")
    llm = ChatOpenAI(temperature=0, )
    tools = load_tools(["requests"])
    tools += [tool]

    agent_chain = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent_chain.run(query)


@app_tool("Zapier Agent")
def zapier_agent(query):
    """Command a specialised Zapier GPT agent a certain action, best for actions that require multiple API calls"""

    llm = OpenAI(temperature=0)
    zapier = ZapierNLAWrapper()
    toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
    actions = zapier.list()
    print(actions)
    agent = initialize_agent(toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent.run(query)
