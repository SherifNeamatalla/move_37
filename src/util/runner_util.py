import json

from src.config.app_config_manager import AppConfigManager
from src.config.constants import JSON_LOADING_ERROR


def validate_last_response(agent):
    """Think about the generated response and see if it's correct"""
    """This method will be called by the runner as a part of the chat loop"""

    try:
        response_json = agent.memory.get_last_agent_message()
        response = json.loads(response_json)
        return response
    except Exception as e:
        # This error will be shown to agent, maybe agent can react to it
        agent.memory.add_tool_error(JSON_LOADING_ERROR, e)
        AppConfigManager().display(JSON_LOADING_ERROR)

        # Return error message, agent will also see this in its short term memory when it acts
        return None
