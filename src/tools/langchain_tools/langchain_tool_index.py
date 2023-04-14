from typing import List

from langchain.agents import Tool

from src.tools.langchain_tools.code_tools import code_tools
from src.tools.langchain_tools.websearch_tools import websearch_tools


def langchain_tools_list() -> List[Tool]:
    """Returns a list of langchain tools used"""
    """To add a new langchain tool, simply add it to the list below"""
    result = []

    result.extend(websearch_tools)
    result.extend(code_tools)

    return result
