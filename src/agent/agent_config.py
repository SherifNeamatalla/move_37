from src.config.constants import BASE_AGENT__TYPE, DEFAULT_TOOLSET_NAME, DEFAULT_MODEL


class AgentConfig:
    def __init__(self, agent_type: str = BASE_AGENT__TYPE, model: str = DEFAULT_MODEL, max_tokens: int = 4096,
                 temperature: float = 0, autonomous: bool = False, toolset_name: str = DEFAULT_TOOLSET_NAME):
        self.config_map = {
            'type': agent_type,
            'model': model,
            'autonomous': autonomous,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'toolset_name': toolset_name,
        }

    def get(self, key: str) -> str:
        return self.config_map[key]

    def to_dict(self) -> dict:
        return self.config_map

    def __dict__(self):
        return self.config_map

    @staticmethod
    def from_dict(dict_input: dict) -> 'AgentConfig':
        return AgentConfig(**dict_input)
