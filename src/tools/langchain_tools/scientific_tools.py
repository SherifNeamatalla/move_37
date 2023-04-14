from langchain import WolframAlphaAPIWrapper
from langchain.agents import Tool

from src.config.env_loader import load_env

load_env()
wolfram = WolframAlphaAPIWrapper()

scientific_tools = [
    Tool(
        name="Wolfram",
        func=wolfram.run,
        description="Run wolfram alpha queries, also suitable for math"
    )
]
