# from src.config.app_config import AppConfig
#
#
# # TODO: should support agent types as well, for now this'll do
# def load_agent_by_id(agent_id):
#     agent = AppConfig().db_manager.get(agent_id)
#     agent = BaseAgent(
#         agent_id=agent['id'],
#         name=agent['name'],
#         role=agent['role'],
#         config=AgentConfig.from_dict(agent['config']),
#         goals=agent['goals'],
#         long_term_memory=agent['long_term_memory'],
#         short_term_memory=agent['short_term_memory']
#     )
#     return agent
#
#
#
# def reset_agent(agent_id):
#     init_app_config(PYTHON_APP_CONFIG_NAME)
#     agent = load_agent_by_id(agent_id)
#     agent.short_term_memory.memory = []
#     agent.save()
#
#
