import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import litellm

DEFAULT_LOG_DIR = Path.home() / ".dasshh" / "logs"
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "dasshh.log"

DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging(log_file=None, log_level=logging.INFO):
    log_file = log_file or DEFAULT_LOG_FILE
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    litellm_logger = litellm.verbose_logger
    root_logger = logging.getLogger()

    for handler in root_logger.handlers[:] + litellm_logger.handlers[:]:
        litellm_logger.removeHandler(handler)
        root_logger.removeHandler(handler)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(log_level)
    litellm_logger.addHandler(file_handler)
    litellm_logger.setLevel(log_level)
    logging.info(f"-- Dasshh logging initialized. Log file: {log_file} --")


def get_logger(name):
    return logging.getLogger(name)
