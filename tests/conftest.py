"""
Shared pytest fixtures and configuration.
"""
import os
import sys
import pytest

# Add the project root directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def cli_runner():
    """Provide a click CLI test runner."""
    from click.testing import CliRunner
    return CliRunner()
