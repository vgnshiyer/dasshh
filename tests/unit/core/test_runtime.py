"""
Tests for the runtime module.
"""
import asyncio
import uuid
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from dasshh.core.runtime import DasshhRuntime, InvocationContext
from dasshh.ui.events import (
    AssistantResponseUpdate,
    AssistantResponseComplete,
    AssistantResponseError,
    AssistantToolCallStart,
)


@pytest.fixture
def runtime(mock_session_service, reset_registry):
    """Create a runtime instance for testing."""
    return DasshhRuntime(mock_session_service)


@pytest.fixture
def invocation_id():
    """Generate a test invocation ID."""
    return str(uuid.uuid4())


@pytest.fixture
def session_id():
    """Generate a test session ID."""
    return str(uuid.uuid4())


@pytest.fixture
def invocation_context(invocation_id, session_id):
    """Create a test invocation context."""
    return InvocationContext(
        invocation_id=invocation_id,
        session_id=session_id,
        message={"role": "user", "content": "Test message"},
        system_instruction=False,
    )


@pytest.fixture
def mock_post_message_callback():
    """Create a mock post_message callback."""
    return MagicMock()


def test_initialization(runtime, mock_session_service):
    """Test initializing the runtime."""
    assert runtime._session_service is mock_session_service
    assert runtime._worker is None
    assert isinstance(runtime._queue, asyncio.Queue)


def test_system_prompt(runtime):
    """Test the system prompt property."""
    system_prompt = runtime.system_prompt
    assert system_prompt["role"] == "system"
    assert "Your name is Dasshh" in system_prompt["content"]


@pytest.mark.asyncio
async def test_start_stop(runtime):
    """Test starting and stopping the runtime."""
    await runtime.start()
    assert runtime._worker is not None
    assert not runtime._worker.done()

    await runtime.stop()
    assert runtime._worker is None


@pytest.mark.asyncio
async def test_submit_query(runtime, invocation_id, session_id, mock_post_message_callback):
    """Test submitting a query to the runtime."""
    with patch("uuid.uuid4", return_value=uuid.UUID(invocation_id)):
        with patch.object(runtime._queue, "put", new_callable=AsyncMock) as mock_put:
            await runtime.submit_query(
                message="Test message",
                session_id=session_id,
                post_message_callback=mock_post_message_callback,
            )

            assert runtime._post_message_callbacks[invocation_id] == mock_post_message_callback
            mock_put.assert_called_once()
            context_arg = mock_put.call_args[0][0]
            assert context_arg.invocation_id == invocation_id
            assert context_arg.session_id == session_id
            assert context_arg.message["role"] == "user"
            assert context_arg.message["content"] == "Test message"
            assert context_arg.system_instruction is False


@pytest.mark.asyncio
async def test_before_query(runtime, invocation_context):
    """Test the _before_query method."""
    runtime._post_message_callbacks[invocation_context.invocation_id] = MagicMock()
    runtime._before_query(invocation_context)

    runtime._session_service.add_event.assert_called_once()
    call_args = runtime._session_service.add_event.call_args[1]
    assert call_args["invocation_id"] == invocation_context.invocation_id
    assert call_args["session_id"] == invocation_context.session_id
    assert call_args["content"]["role"] == "user"
    assert call_args["content"]["content"] == invocation_context.message["content"]


@pytest.mark.asyncio
async def test_during_query(runtime, invocation_context, mock_post_message_callback):
    """Test the _during_query method."""
    runtime._post_message_callbacks[invocation_context.invocation_id] = mock_post_message_callback
    content = "Test response"
    runtime._during_query(invocation_context, content)

    mock_post_message_callback.assert_called_once()
    event = mock_post_message_callback.call_args[0][0]
    assert isinstance(event, AssistantResponseUpdate)
    assert event.invocation_id == invocation_context.invocation_id
    assert event.content == content


@pytest.mark.asyncio
async def test_after_query(runtime, invocation_context, mock_post_message_callback):
    """Test the _after_query method."""
    runtime._post_message_callbacks[invocation_context.invocation_id] = mock_post_message_callback
    content = "Test response"
    runtime._after_query(invocation_context, content)

    runtime._session_service.add_event.assert_called_once()
    call_args = runtime._session_service.add_event.call_args[1]
    assert call_args["invocation_id"] == invocation_context.invocation_id
    assert call_args["session_id"] == invocation_context.session_id
    assert call_args["content"]["role"] == "assistant"
    assert call_args["content"]["content"] == content

    mock_post_message_callback.assert_called_once()
    event = mock_post_message_callback.call_args[0][0]
    assert isinstance(event, AssistantResponseComplete)
    assert event.invocation_id == invocation_context.invocation_id
    assert event.content == content


@pytest.mark.asyncio
async def test_on_query_error(runtime, invocation_context, mock_post_message_callback):
    """Test the _on_query_error method."""
    runtime._post_message_callbacks[invocation_context.invocation_id] = mock_post_message_callback
    error = Exception("Test error")
    runtime._on_query_error(invocation_context, error)

    mock_post_message_callback.assert_called_once()
    event = mock_post_message_callback.call_args[0][0]
    assert isinstance(event, AssistantResponseError)
    assert event.invocation_id == invocation_context.invocation_id
    assert event.error == str(error)


@pytest.mark.asyncio
async def test_before_tool_call(runtime, invocation_context, mock_post_message_callback):
    """Test the _before_tool_call method."""
    runtime._post_message_callbacks[invocation_context.invocation_id] = mock_post_message_callback
    tool_call_id = str(uuid.uuid4())
    tool_name = "test_tool"
    args = '{"test_param": "test_value"}'
    runtime._before_tool_call(invocation_context, tool_call_id, tool_name, args)

    mock_post_message_callback.assert_called_once()
    event = mock_post_message_callback.call_args[0][0]
    assert isinstance(event, AssistantToolCallStart)
    assert event.invocation_id == invocation_context.invocation_id
    assert event.tool_call_id == tool_call_id
    assert event.tool_name == tool_name
    assert event.args == args


@pytest.mark.skip(reason="Requires complex setup with pydantic models")
@pytest.mark.asyncio
async def test_handle_tool_calls(runtime, invocation_context, mock_tool):
    """Test the _handle_tool_calls method."""
    pass
