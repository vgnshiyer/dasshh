from dasshh.core.registry import Registry
from dasshh.core.tools.decorator import tool


@tool
def get_available_tools() -> dict:
    """
    Get all available tools from the registry with their details.

    Returns:
        A list of dictionaries containing tool information (name, description, parameters).
    """
    registry = Registry()
    tools = registry.get_tools()

    return {"available_tools": [tool.get_declaration() for tool in tools]}
