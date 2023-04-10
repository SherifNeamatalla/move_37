from typing import List

from src.tools.base_tool import BaseTool
from src.tools.custom_tools.custom_file_tools import file_tools


def custom_tools_list() -> List[BaseTool]:
    result = []

    result.extend(file_tools)

    return result
