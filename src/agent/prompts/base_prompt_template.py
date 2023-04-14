import json

from src.config.constants import DEFAULT_PROMPT_TEMPLATE_NAME
from src.prompts.prompt_loader import load_prompt_template


class AppBasePromptTemplate:
    """Just a starter simple template"""
    prompt_name = DEFAULT_PROMPT_TEMPLATE_NAME

    def format(self, **kwargs) -> str:
        prompt = load_prompt_template(self.prompt_name)

        prompt = prompt.replace("{name}", kwargs["name"])

        prompt = prompt.replace("{role}", kwargs["role"])

        prompt = prompt.replace("{goals}}", json.dumps(kwargs["goals"]))

        prompt = prompt.replace("{tools}", json.dumps(kwargs["tools"]))

        prompt = prompt.replace("{personal_goals}", kwargs["personal_goals"])

        prompt = prompt.replace("{user_goals}", kwargs["user_goals"])

        prompt = prompt.replace("{summary}", kwargs["summary"])

        prompt = prompt.replace("{context}", kwargs["context"])

        return prompt

    def _prompt_type(self):
        return "base_prompt_template"
