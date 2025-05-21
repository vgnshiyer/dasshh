import json
import os
import yaml
from pathlib import Path
from typing import List
from importlib import import_module

from dasshh.data.models import StorageSession, StorageEvent
from dasshh.ui.types import (
    UISession,
    UIMessage,
    UIAction,
)


DEFAULT_CONFIG_PATH = Path.home() / ".dasshh" / "config.yaml"
DEFAULT_CONFIG = """
app:
  skip_summarization: false
  system_prompt:

model:
  name: gpt-4
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


def load_tools(dir: str = "dasshh.apps") -> None:
    """
    Load all tools from the given directory.
    """
    fs_dir = dir.replace(".", "/")
    for file in os.listdir(fs_dir):
        if file.endswith(".py"):
            import_module(f"{dir}.{file[:-3]}")


def load_config() -> None:
    """Load the configuration file."""
    if DEFAULT_CONFIG_PATH.exists():
        return

    DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_CONFIG_PATH.write_text(DEFAULT_CONFIG)


def get_from_config(key: str) -> dict | str | None:
    """Get a value from the configuration file."""
    if not DEFAULT_CONFIG_PATH.exists():
        return None

    with open(DEFAULT_CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config.get(key, None)
