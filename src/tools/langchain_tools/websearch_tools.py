import os

from langchain import GoogleSerperAPIWrapper, WikipediaAPIWrapper
from langchain.agents import Tool
from langchain.requests import TextRequestsWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper

from src.config.env_loader import load_env
load_env()
search = GoogleSerperAPIWrapper()
wikipedia = WikipediaAPIWrapper()
request = TextRequestsWrapper()
weather = OpenWeatherMapAPIWrapper()
websearch_tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Search for information on google"
    ),
    Tool(
        name="Wiki",
        func=wikipedia.run,
        description="Search for information on wikipedia"
    ),
    Tool(
        name="Request",
        func=request.get,
        description="Get a page raw html"
    ),
    Tool(
        name="Weather",
        func=weather.run,
        description="Get the weather, Format has to be City(Full),Country(2 letter code)"
    )
]
