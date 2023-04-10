from langchain.agents import load_tools

human_tools = [] + load_tools(["human"])
