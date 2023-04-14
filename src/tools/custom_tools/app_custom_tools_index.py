from typing import List

from src.tools.base_tool import BaseTool
from src.tools.custom_tools.custom_browse_tools import browse_tools
from src.tools.custom_tools.custom_file_tools import file_tools


def custom_tools_list() -> List[BaseTool]:
    """Returns a list of custom tools"""
    """To add a new custom tool, simply add it to the list below"""
    result = []

    result.extend(file_tools)
    result.extend(browse_tools)

    return result
