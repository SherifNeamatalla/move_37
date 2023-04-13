from fastapi import Body, HTTPException

from src.agent.agent import Agent
from src.agent.agent_config import AgentConfig
from src.config.app_config_manager import AppConfigManager
from src.config.constants import MISSING_TOOL, MISSING_TOOL_NAME, PERMISSION_DENIED, PERMISSION_GRANTED
from src.runners.python_app_runner import use_tool


def do_list_agents():
    agent_ids = AppConfigManager().list()

    return list(map(lambda agent_id: AppConfigManager().load(agent_id), agent_ids))


# Define the endpoint for your service
def do_create_agent(name: str, role: str, goals: list, config: dict):
    agent = Agent(
        name=name,
        role=role,
        goals=goals,
        config=AgentConfig.from_dict(config)
    )
    AppConfigManager().save(agent)

    return agent.to_dict()


def do_load_agent(agent_id: str):
    return load_agent(agent_id).to_dict()


def do_chat(agent_id: str, message: str = Body(...)):
    agent = load_agent(agent_id)

    response = agent.chat(message)

    if not response:
        raise HTTPException(status_code=500, detail="Agent gave wrong response format")

    AppConfigManager().save(agent)

    return {
        "response": response,
        "agent": agent.to_dict()
    }


def do_act(agent_id: str, body: dict):
    agent = load_agent(agent_id)

    user_response = body['command_response']
    command = body['command']
    if user_response == MISSING_TOOL or user_response == MISSING_TOOL_NAME:
        agent.memory.add_tool_error(user_response)

    # Action denied from user or not accepted, meaning human feedback, again restart loop so agent can react
    elif user_response == PERMISSION_DENIED or not user_response == PERMISSION_GRANTED:
        agent.memory.add_human_feedback(user_response)

    try:
        use_tool(command, agent)
    except Exception as e:
        agent.memory.add_tool_error(e)

    AppConfigManager().save(agent)

    return agent.to_dict()


def load_agent(agent_id):
    agent_dict = AppConfigManager().load(agent_id)
    return Agent.load_from_dict(agent_dict)
