"""
Tests for the base tool class.
"""
import pytest

from dasshh.core.tools.base import BaseTool


class TestTool(BaseTool):
    """Test implementation of BaseTool."""
    def __init__(self, name="test_tool", description="Test tool", parameters=None):
        parameters = parameters or {"type": "object", "properties": {}}
        super().__init__(name, description, parameters)

    def __call__(self, *args, **kwargs):
        return {"result": "test_result"}

    def get_declaration(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }


def test_base_tool_initialization():
    """Test initializing a BaseTool subclass."""
    name = "test_tool"
    description = "A test tool"
    parameters = {"type": "object", "properties": {"test_param": {"type": "string"}}}

    tool = TestTool(name, description, parameters)

    assert tool.name == name
    assert tool.description == description
    assert tool.parameters == parameters


def test_base_tool_call_not_implemented():
    """Test that calling BaseTool directly raises NotImplementedError."""
    tool = BaseTool(
        name="base_tool",
        description="Base tool for testing",
        parameters={"type": "object", "properties": {}}
    )

    with pytest.raises(NotImplementedError, match="This tool has no implementation"):
        tool()


def test_base_tool_get_declaration_not_implemented():
    """Test that get_declaration on BaseTool raises NotImplementedError."""
    tool = BaseTool(
        name="base_tool",
        description="Base tool for testing",
        parameters={"type": "object", "properties": {}}
    )

    with pytest.raises(NotImplementedError, match="This tool has no implementation"):
        tool.get_declaration()


def test_tool_implementation():
    """Test a concrete implementation of BaseTool."""
    tool = TestTool()

    result = tool()
    assert result == {"result": "test_result"}

    declaration = tool.get_declaration()
    assert declaration["type"] == "function"
    assert declaration["function"]["name"] == "test_tool"
    assert declaration["function"]["description"] == "Test tool"
    assert declaration["function"]["parameters"] == {"type": "object", "properties": {}}
