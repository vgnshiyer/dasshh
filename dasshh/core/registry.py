from dasshh.core.tools.base import BaseTool


class Registry:
    """
    A registry for tools.
    """

    _instance: "Registry" = None
    """The singleton instance of the registry."""
    tools: dict[str, BaseTool] = {}
    """The tools in the registry."""

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def add_tool(self, tool: BaseTool):
        """
        Add a tool to the registry.
        """
        if tool.name in self.tools:
            raise ValueError(
                f"Tool name must be unique, there is already a tool named {tool.name}"
            )
        self.tools[tool.name] = tool

    def get_tools(self) -> list[BaseTool]:
        """
        Get all registered tools.
        """
        return list(self.tools.values())

    def get_tool(self, tool_name: str) -> BaseTool | None:
        """
        Get a tool by name.
        """
        return self.tools.get(tool_name, None)

    def get_tool_declarations(self) -> list[dict]:
        """
        Get all registered tool declarations.
        """
        return [tool.get_declaration() for tool in self.get_tools()]
