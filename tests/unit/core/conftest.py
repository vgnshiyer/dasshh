"""
Test fixtures for the core module.
"""
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from dasshh.core.registry import Registry
from dasshh.core.tools.base import BaseTool
from dasshh.data.session import SessionService


@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    with patch("logging.getLogger") as mock_get_logger:
        with patch("logging.FileHandler"), patch("logging.StreamHandler"):
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            yield mock_logger


@pytest.fixture
def test_log_file():
    """Create a temporary log file."""
    fd, path = tempfile.mkstemp()
    try:
        yield path
    finally:
        os.close(fd)
        os.unlink(path)


@pytest.fixture
def reset_registry():
    """Reset the Registry singleton between tests."""
    Registry._instance = None
    Registry.tools = {}
    yield
    Registry._instance = None
    Registry.tools = {}


@pytest.fixture
def mock_tool():
    """Create a mock tool for testing."""
    tool_parameters = {
        "type": "object",
        "properties": {
            "test_param": {
                "type": "string",
                "description": "Test parameter"
            }
        }
    }

    class TestTool(BaseTool):
        def __init__(self):
            super().__init__(
                name="test_tool",
                description="A test tool",
                parameters=tool_parameters
            )

        def __call__(self, test_param=None):
            return {"result": f"Test result with {test_param}"}

        def get_declaration(self):
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": self.parameters
                }
            }

    return TestTool()


@pytest.fixture
def mock_session_service():
    """Create a mock session service for testing."""
    return MagicMock(spec=SessionService)
