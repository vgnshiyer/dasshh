"""
Tests for the function tool class.
"""
import pytest
from unittest.mock import patch

from dasshh.core.tools.function_tool import FunctionTool


def test_function_tool_initialization():
    """Test initializing a FunctionTool."""
    name = "test_function"
    description = "A test function"
    parameters = {"type": "object", "properties": {"test_param": {"type": "string"}}}

    def test_func(test_param=None):
        """A test function."""
        return {"result": f"Test result with {test_param}"}

    tool = FunctionTool(name, description, parameters, func=test_func)

    assert tool.name == name
    assert tool.description == description
    assert tool.parameters == parameters
    assert tool.func == test_func


def test_function_tool_call():
    """Test calling a FunctionTool."""
    def test_func(test_param=None):
        """A test function."""
        return {"result": f"Test result with {test_param}"}

    tool = FunctionTool(
        name="test_function",
        description="A test function",
        parameters={"type": "object", "properties": {}},
        func=test_func
    )

    result = tool(test_param="test_value")

    assert result == {"result": "Test result with test_value"}


def test_function_tool_call_no_implementation():
    """Test calling a FunctionTool with no implementation."""
    tool = FunctionTool(
        name="test_function",
        description="A test function",
        parameters={"type": "object", "properties": {}}
    )

    with pytest.raises(NotImplementedError, match="This tool has no implementation"):
        tool()


def test_function_tool_get_declaration():
    """Test getting the declaration of a FunctionTool."""
    # Define a simple test function
    def test_func(test_param=None):
        """A test function."""
        return {"result": f"Test result with {test_param}"}

    expected_declaration = {
        "name": "test_function",
        "description": "A test function",
        "parameters": {
            "type": "object",
            "properties": {
                "test_param": {
                    "type": "string",
                    "description": "Test parameter"
                }
            }
        }
    }

    with patch(
        "dasshh.core.tools.function_tool.function_to_dict",
        return_value=expected_declaration
    ) as mock_fn_to_dict:
        tool = FunctionTool(
            name="test_function",
            description="A test function",
            parameters={"type": "object", "properties": {}},
            func=test_func
        )

        declaration = tool.get_declaration()

        mock_fn_to_dict.assert_called_once_with(test_func)

        assert declaration == expected_declaration
