"""
Tests for the registry module.
"""
import pytest
from unittest.mock import Mock

from dasshh.core.registry import Registry
from dasshh.core.tools.base import BaseTool


def test_registry_singleton(reset_registry):
    """Test that Registry is a singleton."""
    registry1 = Registry()
    registry2 = Registry()
    assert registry1 is registry2

    tool = Mock(spec=BaseTool)
    tool.name = "test_tool"
    registry1.add_tool(tool)

    assert "test_tool" in registry2.tools


def test_add_tool(reset_registry, mock_tool):
    """Test adding a tool to the registry."""
    registry = Registry()

    registry.add_tool(mock_tool)

    assert mock_tool.name in registry.tools
    assert registry.tools[mock_tool.name] is mock_tool


def test_add_duplicate_tool(reset_registry, mock_tool):
    """Test adding a tool with a duplicate name."""
    registry = Registry()
    registry.add_tool(mock_tool)

    duplicate_tool = Mock(spec=BaseTool)
    duplicate_tool.name = mock_tool.name

    with pytest.raises(ValueError, match=f"Tool name must be unique, there is already a tool named {mock_tool.name}"):
        registry.add_tool(duplicate_tool)


def test_get_tools(reset_registry, mock_tool):
    """Test getting all tools from the registry."""
    registry = Registry()
    registry.add_tool(mock_tool)
    tools = registry.get_tools()
    assert len(tools) == 1
    assert tools[0] is mock_tool


def test_get_tool(reset_registry, mock_tool):
    """Test getting a specific tool by name."""
    registry = Registry()
    registry.add_tool(mock_tool)
    tool = registry.get_tool(mock_tool.name)
    assert tool is mock_tool


def test_get_nonexistent_tool(reset_registry):
    """Test getting a tool that doesn't exist."""
    registry = Registry()
    tool = registry.get_tool("nonexistent_tool")
    assert tool is None


def test_get_tool_declarations(reset_registry, mock_tool):
    """Test getting tool declarations."""
    registry = Registry()
    registry.add_tool(mock_tool)
    declarations = registry.get_tool_declarations()
    assert len(declarations) == 1
    assert declarations[0] == mock_tool.get_declaration()
