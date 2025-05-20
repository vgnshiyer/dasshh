"""Tests for the UI types module."""
import datetime
import pytest
from pydantic import ValidationError

from dasshh.ui.types import UIMessage, UIAction, UISession


def test_ui_message_initialization():
    """Test that UIMessage can be initialized with valid parameters."""
    message = UIMessage(
        invocation_id="test_id",
        role="user",
        content="Hello, world!"
    )
    
    assert message.invocation_id == "test_id"
    assert message.role == "user"
    assert message.content == "Hello, world!"


def test_ui_message_default_invocation_id():
    """Test that UIMessage initializes with empty string as default invocation_id."""
    message = UIMessage(role="assistant", content="Hello!")
    
    assert message.invocation_id == ""
    assert message.role == "assistant"
    assert message.content == "Hello!"


def test_ui_message_invalid_role():
    """Test that UIMessage validates role field."""
    with pytest.raises(ValidationError):
        UIMessage(role="invalid_role", content="Hello!")


def test_ui_action_initialization():
    """Test that UIAction can be initialized with valid parameters."""
    action = UIAction(
        tool_call_id="tool_1",
        invocation_id="inv_1",
        name="test_tool",
        args='{\n  "param": "value"\n}',
        result='{\n  "result": "success"\n}'
    )
    
    assert action.tool_call_id == "tool_1"
    assert action.invocation_id == "inv_1"
    assert action.name == "test_tool"
    assert action.args == '{\n  "param": "value"\n}'
    assert action.result == '{\n  "result": "success"\n}'


def test_ui_session_initialization():
    """Test that UISession can be initialized with valid parameters."""
    now = datetime.datetime.now()
    
    session = UISession(
        id="session_1",
        detail="Test session",
        created_at=now,
        updated_at=now,
        messages=[
            UIMessage(role="user", content="Hello")
        ],
        actions=[
            UIAction(
                tool_call_id="tool_1",
                invocation_id="inv_1",
                name="test_tool",
                args='{}',
                result='{}'
            )
        ]
    )
    
    assert session.id == "session_1"
    assert session.detail == "Test session"
    assert session.created_at == now
    assert session.updated_at == now
    assert len(session.messages) == 1
    assert len(session.actions) == 1
    assert session.messages[0].role == "user"
    assert session.actions[0].name == "test_tool" 