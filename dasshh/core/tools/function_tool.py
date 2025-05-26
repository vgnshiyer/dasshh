from typing import Callable
from litellm.utils import function_to_dict

from dasshh.core.tools.base import BaseTool


class FunctionTool(BaseTool):
    """
    A tool is a function that can be used to help the user.
    """

    func: Callable = None
    """The function of the tool."""

    def __init__(
        self, name: str, description: str, parameters: dict, func: Callable = None
    ):
        super().__init__(name, description, parameters)
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.func:
            return self.func(*args, **kwargs)
        raise NotImplementedError("This tool has no implementation")

    def get_declaration(self) -> dict:
        """
        Get the declaration of the tool.
        """
        return function_to_dict(self.func)
