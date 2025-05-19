import json
from typing import List
from dasshh.data.models import StorageSession, StorageEvent
from dasshh.ui.dto import (
    UISession,
    UIMessage,
    UIAction,
)


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
