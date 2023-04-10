from langchain.agents import Tool

from src.tools.base_tool import BaseTool
from src.tools.custom_tools.app_custom_tools_index import custom_tools_list
from src.tools.huggingface_tools.huggingface_tools_index import huggingface_tools_list
from src.tools.indexing_tools.indexing_tools_index import indexing_tools_list
from src.tools.langchain_tools.langchain_tool_index import langchain_tools_list


# Find the correct tool manager/format and execute the tool
# Can be: Custom format, similar to langchain but accepts a dict instead of a string
#         Langchain format
#         Indexing format, planned to use indexers to search data, prob through a specialised agent
def run_tool(tool: dict) -> str:
    """Use a tool"""
    if not tool or 'name' not in tool or not tool['name']:
        return 'Error: Missing tool name'

    args = tool['args'] if 'args' in tool else {}

    tool_name = tool['name']

    # Try to find it in custom tools
    custom_tools = custom_tools_list()

    langchain_tools = langchain_tools_list()

    indexing_tools = indexing_tools_list()

    huggingface_tools = huggingface_tools_list()

    try:
        tool = next(t for t in custom_tools if t.name == tool_name)
    except StopIteration:
        tool = next(t for t in langchain_tools if t.name == tool_name)
    except StopIteration:
        tool = next(t for t in indexing_tools if t.name == tool_name)
    except StopIteration:
        tool = next(t for t in huggingface_tools if t.name == tool_name)
    except StopIteration:
        return 'Error: Tool not found'

    return execute(tool, args)


def execute(tool: BaseTool | Tool, tool_args: str) -> str:
    # TODO add support for indexing

    if isinstance(tool, BaseTool):
        tool_args.split(',')
        return tool.run(tool_args)

    if isinstance(tool, Tool):
        return tool.run(tool_args)
