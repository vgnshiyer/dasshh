from abc import ABC


class BaseTool(ABC):
    """
    Base class for all tools.
    """

    name: str
    """The name of the tool."""
    description: str
    """The description of the tool."""
    parameters: dict
    """The parameters of the tool."""

    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("This tool has no implementation")

    def get_declaration(self) -> dict:
        """
        Get the declaration of the tool.
        """
        raise NotImplementedError("This tool has no implementation")
