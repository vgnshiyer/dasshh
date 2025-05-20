"""
Tests for the main CLI entry point.
"""
from unittest.mock import patch

from dasshh.__main__ import main


def test_version_option(cli_runner):
    """Test the --version option."""
    result = cli_runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


@patch("dasshh.ui.app.Dasshh")
def test_main_no_command(mock_dasshh, cli_runner):
    """Test invoking the main CLI without a subcommand."""
    mock_app_instance = mock_dasshh.return_value
    result = cli_runner.invoke(main)
    assert mock_dasshh.called
    assert mock_app_instance.run.called
    assert result.exit_code == 0
