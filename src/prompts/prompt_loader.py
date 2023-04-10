import os

from src.config.constants import PROMPTS_TEMPLATES_DIR, TOOLSETS_DIR
from src.logger.logger import log


def load_toolset(toolset_filename):
    try:
        # get directory of this file:
        toolset_path = os.path.join(TOOLSETS_DIR, toolset_filename)
        # Load the prompt from prompts/prompt.txt
        with open(toolset_path, "r") as prompt_file:
            prompt = prompt_file.read()

        return prompt
    except FileNotFoundError:
        log("Error: Prompt file not found")
        return ""


def load_prompt_template(prompt_file_name):
    try:
        # get directory of this file:
        prompt_template_path = os.path.join(PROMPTS_TEMPLATES_DIR, prompt_file_name)
        # Load the prompt from prompts/prompt.txt
        with open(prompt_template_path, "r") as prompt_file:
            prompt = prompt_file.read()

        return prompt
    except FileNotFoundError:
        log("Error: Prompt file not found")
        return ""
