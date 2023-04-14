from typing import List

from langchain.agents import Tool

from src.tools.indexing_tools.langchain_indexing_tools import langchain_indexing_tools


def single_function_agents_list() -> List[Tool]:
    """Returns a list of indexing tools built upon langchain indexing"""
    """Should be called when the request has attachment or needs indexing"""
    """To add a new indexing tool, simply add it to the list below"""""
    result = []

    # result.extend()

    return result
