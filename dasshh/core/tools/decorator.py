from typing import Callable

from dasshh.core.registry import Registry
from dasshh.core.tools.function_tool import FunctionTool


def tool(func: Callable):
    """
    A decorator to convert a function into a tool.
    """

    tool_instance = FunctionTool(
        name=func.__name__,
        description=func.__doc__,
        parameters=func.__annotations__,
        func=func,
    )

    registry = Registry()
    registry.add_tool(tool_instance)

    return tool_instance
