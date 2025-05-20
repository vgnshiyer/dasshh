"""Tests for the UI events module."""

from dasshh.ui.events import (
    ChangeView,
    NewMessage,
    NewSession,
    LoadSession,
    DeleteSession,
    AssistantResponseStart,
    AssistantResponseUpdate,
    AssistantResponseComplete,
    AssistantResponseError,
    AssistantToolCallStart,
    AssistantToolCallComplete,
    AssistantToolCallError,
)


def test_change_view_event():
    """Test initialization of ChangeView event."""
    event = ChangeView("chat")
    assert event.view == "chat"


def test_new_message_event():
    """Test initialization of NewMessage event."""
    message = "Hello, world!"
    event = NewMessage(message)
    assert event.message == message


def test_new_session_event():
    """Test initialization of NewSession event."""
    event = NewSession()
    assert isinstance(event, NewSession)


def test_load_session_event():
    """Test initialization of LoadSession event."""
    session_id = "test_session_id"
    event = LoadSession(session_id)
    assert event.session_id == session_id


def test_delete_session_event():
    """Test initialization of DeleteSession event."""
    session_id = "test_session_id"
    event = DeleteSession(session_id)
    assert event.session_id == session_id


def test_assistant_response_start_event():
    """Test initialization of AssistantResponseStart event."""
    invocation_id = "test_invocation_id"
    event = AssistantResponseStart(invocation_id)
    assert event.invocation_id == invocation_id


def test_assistant_response_update_event():
    """Test initialization of AssistantResponseUpdate event."""
    invocation_id = "test_invocation_id"
    content = "Partial response content"
    event = AssistantResponseUpdate(invocation_id, content)
    assert event.invocation_id == invocation_id
    assert event.content == content


def test_assistant_response_complete_event():
    """Test initialization of AssistantResponseComplete event."""
    invocation_id = "test_invocation_id"
    content = "Complete response content"
    event = AssistantResponseComplete(invocation_id, content)
    assert event.invocation_id == invocation_id
    assert event.content == content


def test_assistant_response_error_event():
    """Test initialization of AssistantResponseError event."""
    invocation_id = "test_invocation_id"
    error = "Error message"
    event = AssistantResponseError(invocation_id, error)
    assert event.invocation_id == invocation_id
    assert event.error == error


def test_assistant_tool_call_start_event():
    """Test initialization of AssistantToolCallStart event."""
    invocation_id = "test_invocation_id"
    tool_call_id = "test_tool_call_id"
    tool_name = "test_tool"
    args = '{"param": "value"}'
    
    event = AssistantToolCallStart(invocation_id, tool_call_id, tool_name, args)
    
    assert event.invocation_id == invocation_id
    assert event.tool_call_id == tool_call_id
    assert event.tool_name == tool_name
    assert event.args == args


def test_assistant_tool_call_complete_event():
    """Test initialization of AssistantToolCallComplete event."""
    invocation_id = "test_invocation_id"
    tool_call_id = "test_tool_call_id"
    tool_name = "test_tool"
    result = '{"result": "success"}'
    
    event = AssistantToolCallComplete(invocation_id, tool_call_id, tool_name, result)
    
    assert event.invocation_id == invocation_id
    assert event.tool_call_id == tool_call_id
    assert event.tool_name == tool_name
    assert event.result == result


def test_assistant_tool_call_error_event():
    """Test initialization of AssistantToolCallError event."""
    invocation_id = "test_invocation_id"
    tool_call_id = "test_tool_call_id"
    tool_name = "test_tool"
    error = "Tool call error message"
    
    event = AssistantToolCallError(invocation_id, tool_call_id, tool_name, error)
    
    assert event.invocation_id == invocation_id
    assert event.tool_call_id == tool_call_id
    assert event.tool_name == tool_name
    assert event.error == error 