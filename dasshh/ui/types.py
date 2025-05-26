from datetime import datetime
from typing import Literal, List
from pydantic import BaseModel, Field


class UIMessage(BaseModel):
    """A message to be displayed in the UI."""

    invocation_id: str = Field("", description="The invocation id of the message.")
    role: Literal["user", "assistant"] = Field(
        ..., description="The role of the message."
    )
    content: str = Field(..., description="The content of the message.")


class UIAction(BaseModel):
    """An action to be displayed in the UI."""

    tool_call_id: str = Field(..., description="The tool call id of the action.")
    invocation_id: str = Field(..., description="The invocation id of the action.")
    name: str = Field(..., description="The name of the action.")
    args: str = Field(
        ...,
        description="The arguments of the action. This has to be a JSON string with indent=2.",
    )
    result: str = Field(
        ...,
        description="The result of the action. This has to be a JSON string with indent=2.",
    )


class UISession(BaseModel):
    """A session to be displayed in the UI."""

    id: str = Field(..., description="The id of the session.")
    detail: str = Field(..., description="The detail of the session.")
    created_at: datetime = Field(..., description="The creation time of the session.")
    updated_at: datetime = Field(
        ..., description="The last update time of the session."
    )
    messages: List[UIMessage] = Field(..., description="The messages of the session.")
    actions: List[UIAction] = Field(..., description="The actions of the session.")
