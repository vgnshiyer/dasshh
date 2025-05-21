import json
import os
import sys
import yaml
from pathlib import Path
from typing import List
from importlib import import_module
import importlib.resources as pkg_resources

from dasshh.data.models import StorageSession, StorageEvent
from dasshh.ui.types import (
    UISession,
    UIMessage,
    UIAction,
)
from dasshh.core.logging import get_logger

logger = get_logger(__name__)


DEFAULT_CONFIG_PATH = Path.home() / ".dasshh" / "config.yaml"
try:
    DASSHH_EXEC_PATH = str(Path(pkg_resources.files('dasshh')))
except (ImportError, TypeError):
    DASSHH_EXEC_PATH = str(Path(__file__).parent.parent)

DEFAULT_TOOLS_PATH = str(Path(DASSHH_EXEC_PATH) / "apps")

DEFAULT_CONFIG = f"""
dasshh:
  skip_summarization: false
  system_prompt:
  tool_directories:
    - {DEFAULT_TOOLS_PATH}

model:
  name: gemini/gemini-2.0-flash
  api_base:
  api_key:
  api_version:
  temperature: 1.0
  top_p: 1.0
  max_tokens:
  max_completion_tokens:
"""


def convert_session_obj(session_obj: StorageSession, events: List[StorageEvent] | None = None) -> UISession:
    messages, actions = [], {}
    if events:
        for event in events:
            invocation_id = event.invocation_id
            content = event.content
            if content["role"] == "assistant" and "tool_calls" in content:
                for tool_call in content["tool_calls"]:
                    tool_call_id = tool_call["id"]
                    args = json.dumps(json.loads(tool_call["function"]["arguments"]), indent=2)
                    actions[tool_call_id] = UIAction(
                        invocation_id=invocation_id,
                        tool_call_id=tool_call_id,
                        name=tool_call["function"]["name"],
                        args=args,
                        result="",
                    )
            elif content["role"] == "tool":
                tool_call_id = content["tool_call_id"]
                actions[tool_call_id].result = content["content"]
            elif content["role"] in ["user", "assistant"]:
                messages.append(
                    UIMessage(invocation_id=invocation_id, role=content["role"], content=content["content"])
                )
    return UISession(
        id=session_obj.id,
        detail=session_obj.detail,
        created_at=session_obj.created_at,
        updated_at=session_obj.updated_at,
        messages=messages,
        actions=list(actions.values()),
    )


def load_tools() -> None:
    """
    Load all tools from the given directories recursively.

    Args:
        dirs: A list of directory paths to load tools from (absolute file paths).
              If None, will use paths from config or fall back to default.
    """
    tool_dirs_config = get_from_config("dasshh.tool_directories")
    if tool_dirs_config:
        dirs = tool_dirs_config
    else:
        dirs = [DEFAULT_TOOLS_PATH]

    for dir_path in dirs:
        if os.path.exists(dir_path):
            for root, dirs, files in os.walk(dir_path):
                if "__init__.py" in files:
                    # Determine full module path
                    rel_path = os.path.relpath(root, dir_path)
                    if rel_path == ".":
                        module_path = os.path.basename(dir_path)
                        module_parent = os.path.dirname(dir_path)
                    else:
                        module_path = rel_path.replace(os.sep, ".")
                        module_parent = dir_path

                    if module_parent not in sys.path:
                        sys.path.append(module_parent)

                    try:
                        import_module(module_path)
                        logger.info(f"Imported module: {module_path}")
                    except ImportError as e:
                        logger.error(f"Failed to import {module_path}: {e}")


def load_config() -> None:
    """Load the configuration file."""
    if DEFAULT_CONFIG_PATH.exists():
        return

    DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_CONFIG_PATH.write_text(DEFAULT_CONFIG)


def get_from_config(key: str) -> dict | str | List | None:
    """Get a value from the configuration file."""
    if not DEFAULT_CONFIG_PATH.exists():
        return None

    with open(DEFAULT_CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    if '.' in key:
        parts = key.split('.')
        curr = config
        for part in parts:
            if curr is None or part not in curr:
                return None
            curr = curr.get(part)
        return curr

    return config.get(key, None)
