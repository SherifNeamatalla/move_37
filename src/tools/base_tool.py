from typing import Callable, Optional, Awaitable, Any


# Copied from langchain tools
class BaseTool:
    """Command that takes in function or coroutine directly."""

    description: str = ""
    func: Callable
    coroutine: Optional[Callable[[str], Awaitable[str]]] = None

    def __init__(self, name: str, func: Callable, description: str, **kwargs: Any) -> None:
        self.name = name
        self.func = func
        self.description = description
        self.kwargs = kwargs

    def run(self, tool_input: dict) -> str:
        """Use the tool."""
        return self.func(**tool_input)

    async def arun(self, tool_input: str) -> str:
        """Use the tool asynchronously."""
        if self.coroutine:
            return await self.coroutine(tool_input)
        raise NotImplementedError("Command does not support async")
