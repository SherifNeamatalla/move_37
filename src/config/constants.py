import os
from pathlib import Path

###Directories###
FILES_DIR = os.path.join(Path(__file__).parent.parent, "storage", "files")
PROMPTS_DIR = os.path.join(Path(__file__).parent.parent, "prompts")
PROMPTS_TEMPLATES_DIR = os.path.join(Path(__file__).parent.parent, "prompts", "templates")
TOOLSETS_DIR = os.path.join(Path(__file__).parent.parent, "prompts", "toolsets")
AGENTS_DIR = os.path.join(Path(__file__).parent.parent, "storage", "agents")
####Roles####
USER_ROLE = "user"
SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"

###Agent Feedback###
MISSING_TOOL_NAME = "You forgot to send to the tool name, try again and stick to the rules specified above"
MISSING_TOOL = "You forgot to send a tool, try again and stick to the rules specified above"

###Agents Types###
BASE_AGENT__TYPE = "BaseAgent"

###Model Defaults###
DEFAULT_MODEL = "gpt-3.5-turbo"
RESPONSE_TOKEN_RESERVE = 1000

####Default Prompts and Configs####
DEFAULT_TOOLSET_NAME = "base_toolset.txt"
DEFAULT_PROMPT_TEMPLATE_NAME = "base_prompt_template.txt"
DEFAULT_EMPTY_USER_INPUT_TEMPLATE_NAME = "empty_user_input_template.txt"
DEFAULT_USER_INPUT_TEMPLATE = "user_input_template.txt"
####Response Errors####
PERMISSION_DENIED = "Action denied"
PERMISSION_GRANTED = "Permission granted"
JSON_LOADING_ERROR = "JSON loading error, please stick to the format specified above. Your request has to contain " \
                     "only JSON, nothing before nothing after."
