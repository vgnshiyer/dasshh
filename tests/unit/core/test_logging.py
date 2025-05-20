"""
Tests for the logging module.
"""
from pathlib import Path
from unittest.mock import patch, MagicMock

from dasshh.core.logging import get_logger, DEFAULT_LOG_DIR, DEFAULT_LOG_FILE


def test_get_logger():
    """Test get_logger function."""
    with patch('logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        logger = get_logger("test_logger")
        mock_get_logger.assert_called_once_with("test_logger")
        assert logger == mock_logger


def test_default_log_dir_exists():
    """Test that the default log directory exists."""
    assert DEFAULT_LOG_DIR.exists()
    assert DEFAULT_LOG_DIR == Path.home() / ".dasshh" / "logs"


def test_default_log_file_path():
    """Test the default log file path."""
    assert DEFAULT_LOG_FILE == DEFAULT_LOG_DIR / "dasshh.log"
