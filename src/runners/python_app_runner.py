import json

from src.agent.agent import Agent
from src.agent.agent_config import AgentConfig
from src.config.app_config_manager import AppConfigManager
from src.config.constants import JSON_LOADING_ERROR, MISSING_TOOL_NAME, MISSING_TOOL, PERMISSION_DENIED, \
    PERMISSION_GRANTED
from src.display.command_line_display_manager import CommandLineDisplayManager
from src.display.spinner import Spinner
from src.runners.runner_interface import IRunner
from src.tools.tools_manager import run_tool


def write(thoughts):
    AppConfigManager().display_manager.print(thoughts['summary'])

    AppConfigManager().display_manager.print(thoughts['reasoning'])


def speak(thoughts):
    if not AppConfigManager().voice_manager:
        return

    AppConfigManager().voice_manager.say(thoughts['speak'])


def plan(thoughts, goals):
    personal_goals = thoughts['goals'].split('\n')

    AppConfigManager().display_manager.print(f"Goals:\n{goals},\n Personal goals:\n{goals}")


def ask_user_permission(response, agent):
    suggested_tool = response['tool']

    thoughts = response['thoughts']

    write(thoughts)

    speak(thoughts)

    plan(thoughts, agent.goals)

    user_response = ask_user_tool_permission(agent.name, suggested_tool)

    return user_response, suggested_tool


def use_tool(tool, agent):
    tool_name = tool['name']
    tool_args = tool.get('args', [])
    tool_type = tool.get('type', None)
    AppConfigManager().display_manager.print(
        f"Using tool {tool_name} with args {tool_args} and type {tool_type}")

    tool_result = run_tool(tool)

    AppConfigManager().display_manager.print(f"Command {tool_name},\n Result: {tool_result}")

    agent.memory.add_tool_result(tool_name, tool_result)

    return tool_result


class PythonAppRunner(IRunner):

    def __init__(self):
        AppConfigManager(
            display_manager=CommandLineDisplayManager(),
        )

    def run(self):
        agent = load_agent()

        AppConfigManager().display_manager.print(f"Hello world! I'm {agent.name}!")

        while True:
            with Spinner("Thinking... "):
                agent.chat()

            response = validate_last_response(agent)

            # If response is none this is an error, chat again so they can react to it as the error was added to history
            if response is None:
                continue

            user_response, suggested_tool = ask_user_permission(response, agent)

            # This means missing tool or tool name, restart loop so agent can react
            if user_response == MISSING_TOOL or user_response == MISSING_TOOL_NAME:
                agent.memory.add_tool_error(user_response)
                AppConfigManager().display_manager.print(user_response)
                continue

            # Action denied from user or not accepted, meaning human feedback, again restart loop so agent can react
            if user_response == PERMISSION_DENIED or not user_response == PERMISSION_GRANTED:
                agent.memory.add_human_feedback(user_response)
                continue

            try:
                use_tool(suggested_tool, agent)
            except Exception as e:
                agent.memory.add_tool_error(e)

            AppConfigManager().display_manager.print(suggested_tool)

            AppConfigManager().save(agent)


def ask_user_tool_permission(agent_name, tool):
    if not tool:
        # When agent has no output tool, this usually means they're going to an infinite loop
        return MISSING_TOOL

    if 'name' not in tool or not tool['name']:
        # When agent has no output tool, this usually means they're going to an infinite loop
        return MISSING_TOOL_NAME

    return ask_for_permission(agent_name, tool)


def ask_for_permission(name, tool, autonomous=False):
    if not autonomous:
        user_input = AppConfigManager().display_manager.prompt(name, tool)

        if user_input == 'n':
            return PERMISSION_DENIED

        if user_input == 'y':
            return PERMISSION_GRANTED

        return user_input

    return PERMISSION_GRANTED


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
        AppConfigManager().display_manager.print(JSON_LOADING_ERROR)

        # Return error message, agent will also see this in its short term memory when it acts
        return None


def load_agent():
    load = AppConfigManager().display_manager.prompt("Load agent? (y/n): ")

    ##TODO load agent
    if load == "y":
        pass
        existing_agents_names = AppConfigManager().list()

        # Show agents and get user input
        for i, agent_name in enumerate(existing_agents_names):
            print(f"{i}: {agent_name}")

        agent_index = None

        while agent_index is None or not isinstance(agent_index, int) or int(agent_index) >= len(
                existing_agents_names) or int(agent_index) < 0:
            try:
                agent_index = int(AppConfigManager().display_manager.prompt(
                    "Enter a valid index for an existing agent: "))
            except ValueError:
                agent_index = None

        agent_dict = AppConfigManager().load(existing_agents_names[agent_index])

        agent = Agent.load_from_dict(agent_dict)

    else:
        # Get user input to initialize the agent
        name = AppConfigManager().display_manager.prompt("Enter the name of the agent: ")

        role = AppConfigManager().display_manager.prompt("Enter the role of the agent: ")

        goals = []

        while True:
            goal = AppConfigManager().display_manager.prompt(
                "Enter a goal for the agent (leave blank to finish): ")
            if goal == "":
                break
            goals.append(goal)

        config = AgentConfig()

        # agent_id = AppConfigManager().db_manager.add(name, role, goals, config)

        # Initialize the agent
        agent = Agent(name=name, role=role, config=config, goals=goals)

    return agent
