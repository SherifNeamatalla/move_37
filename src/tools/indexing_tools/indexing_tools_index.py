from typing import List

from langchain.agents import Tool
from langchain.indexes import VectorstoreIndexCreator

from src.tools.indexing_tools.langchain_indexing_tools import loaders_map


def indexing_tools_list() -> List[Tool]:
    """Returns a list of indexing tools built upon langchain indexing"""
    """Should be called when the request has attachment or needs indexing"""
    """To add a new indexing tool, simply add it to the list below"""""
    result = []

    result.extend(loaders_map.keys())

    return result


def execute_indexing(name: str, query: str, kwargs=None):
    """Execute an indexing tool"""
    if kwargs is None:
        kwargs = {}

    if name not in loaders_map:
        return "Error: Indexing tool not found"

    loader = loaders_map[name]

    loader(**kwargs)

    index = VectorstoreIndexCreator().from_loaders([loader])

    return index.query(query)
