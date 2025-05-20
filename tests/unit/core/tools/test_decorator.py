"""
Tests for the tool decorator.
"""
from unittest.mock import patch, MagicMock

from dasshh.core.tools.decorator import tool
from dasshh.core.tools.function_tool import FunctionTool


def test_tool_decorator():
    """Test the @tool decorator."""
    mock_registry = MagicMock()

    def test_function(param1: str = "default") -> dict:
        """Test function docstring."""
        return {"result": param1}

    with patch("dasshh.core.tools.decorator.Registry", return_value=mock_registry):
        decorated = tool(test_function)

        assert isinstance(decorated, FunctionTool)

        mock_registry.add_tool.assert_called_once_with(decorated)

        assert decorated.name == "test_function"
        assert decorated.description == "Test function docstring."
        assert decorated.func == test_function

        assert decorated.parameters == test_function.__annotations__

        result = decorated(param1="test")
        assert result == {"result": "test"}


def test_tool_decorator_integration():
    """Test the @tool decorator in a more realistic scenario."""
    with patch("dasshh.core.tools.decorator.Registry") as MockRegistry:
        mock_registry_instance = MagicMock()
        MockRegistry.return_value = mock_registry_instance

        @tool
        def example_tool(param1: str = "default") -> dict:
            """Example tool docstring."""
            return {"result": param1}

        assert isinstance(example_tool, FunctionTool)

        mock_registry_instance.add_tool.assert_called_once()

        result = example_tool(param1="test_value")
        assert result == {"result": "test_value"}
