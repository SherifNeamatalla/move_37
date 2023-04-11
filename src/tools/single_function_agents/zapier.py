import json
import os
from typing import List, Dict

import requests
from langchain import PromptTemplate
from requests import Request, Session

from src.agent.single_use_agent import SingleUserAgent
from src.config.env_loader import load_env
from src.prompts.prompt_loader import load_prompt_template
from src.tools.tool_annotation import app_tool

LIST_TOOLS_URL = "https://nla.zapier.com/api/v1/dynamic/exposed/"

load_env()
access_token = os.environ["ZAPIER_NLA_API_KEY"]
headers = {"Authorization": f"Bearer {access_token}"}

zapier_nla_api_base: str = "https://nla.zapier.com/api/v1/"

ZAPIER_MANAGER_PROMPT_TEMPLATE_NAME = "zapier_manager_prompt_template.txt"
ZAPIER_USER_INPUT_TEMPLATE_NAME = "zapier_user_input_template.txt"
ZAPIER_IMPOSSIBLE_ACTION = "IMPOSSIBLE"


# TODO :add review

@app_tool("Zapier Agent")
def zapier_agent(query):
    """Command a specialised Zapier GPT agent a certain action, best for actions that require multiple API calls"""

    actions = list_actions()

    zapier_agent_input = zapier_manager_agent("Fetch me the latest email from erika drumming", actions)

    if zapier_agent_input["operation"]["id"] == ZAPIER_IMPOSSIBLE_ACTION:
        return "This action cannot be executed given the current available Zapier operations."

    if not zapier_agent_input["operation"]["args"]:
        zapier_agent_input["operation"]["args"] = {}

    zapier_response = execute_action(zapier_agent_input["operation"]['id'], zapier_agent_input['operation']["args"])

    response = zapier_response.json()

    return {
        "action_used": response["action_used"],
        "input_params": response["input_params"],
        "result": response["result"],
        "status": response["status"],
        "error": response["error"],
    }


def zapier_manager_agent(user_input, actions):
    user_input_template = PromptTemplate(template=load_prompt_template(ZAPIER_USER_INPUT_TEMPLATE_NAME),
                                         input_variables=["user_input"])

    prompt_template = PromptTemplate(template=load_prompt_template(ZAPIER_MANAGER_PROMPT_TEMPLATE_NAME),
                                     input_variables=["zapier_actions"])
    agent = SingleUserAgent(prompt_template=prompt_template, user_input_template=user_input_template)

    response_json = agent.chat(prompt_input={
        "zapier_actions": actions
    },
        user_input=user_input)

    return json.loads(response_json)


def list_actions() -> List[Dict]:
    session = get_session()
    response = session.get(zapier_nla_api_base + "exposed/")
    response.raise_for_status()
    actions = response.json()["results"]

    return list(map(lambda action: {
        "operation_id": action["id"],
        "description": action["description"],
        "operation_name": action["operation_id"],
        "params": action["params"]
    }, actions))


def get_openapi_schema():
    url = "https://nla.zapier.com/api/v1/openapi.json"
    response = requests.get(url, headers=headers)
    return response.json()


# exposed/{action_id}/execute/
def execute_action(action_id, payload):
    url = f"https://nla.zapier.com/api/v1/exposed/{action_id}/execute/"
    session = get_session()
    request = Request(
        "POST",
        url,
        json=payload
    )
    return session.send(session.prepare_request(request))


def get_session() -> Session:
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    session.params = {"api_key": access_token}
    return session
