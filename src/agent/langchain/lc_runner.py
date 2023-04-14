from typing import Optional, List

from src.agent.langchain.langchain_agent import LangchainAgent


def run(name: str, role: str, task: str, goals: Optional[List[str]] = None):
    agent = LangchainAgent(name, role, goals)


