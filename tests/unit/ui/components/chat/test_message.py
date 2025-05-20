"""Tests for the ChatMessage component."""
from rich.console import Group
from rich.markdown import Markdown
from rich.text import Text

from dasshh.ui.components.chat.message import ChatMessage


def test_chat_message_initialization_user():
    """Test ChatMessage initialization with user role."""
    message = ChatMessage(
        invocation_id="test_id",
        role="user",
        content="Hello, world!"
    )
    
    assert message.invocation_id == "test_id"
    assert message.role == "you"
    assert message.content == "Hello, world!"
    
    # Check CSS class was added
    assert "user" in message.classes


def test_chat_message_initialization_assistant():
    """Test ChatMessage initialization with assistant role."""
    message = ChatMessage(
        invocation_id="test_id",
        role="assistant",
        content="Hello, I'm the assistant!"
    )
    
    assert message.invocation_id == "test_id"
    assert message.role == "dasshh"
    assert message.content == "Hello, I'm the assistant!"
    
    # Check CSS class was added
    assert "assistant" in message.classes


def test_chat_message_render_user():
    """Test rendering a user message."""
    message = ChatMessage(
        invocation_id="test_id",
        role="user",
        content="Hello, world!"
    )
    
    rendered = message.render()
    
    # Check that the rendered output is a Group
    assert isinstance(rendered, Group)
    
    # The Group should contain a title and content
    assert len(rendered.renderables) == 2
    
    # Check the title contains the role capitalized
    title = rendered.renderables[0]
    assert isinstance(title, Text)
    assert "You" in title.plain
    
    # Check the content is formatted as Markdown
    content = rendered.renderables[1]
    assert isinstance(content, Markdown)
    assert content.markup == "Hello, world!"


def test_chat_message_render_assistant():
    """Test rendering an assistant message."""
    message = ChatMessage(
        invocation_id="test_id",
        role="assistant",
        content="Hello, I'm the assistant!"
    )
    
    rendered = message.render()
    
    # Check that the rendered output is a Group
    assert isinstance(rendered, Group)
    
    # The Group should contain a title and content
    assert len(rendered.renderables) == 2
    
    # Check the title contains the role capitalized
    title = rendered.renderables[0]
    assert isinstance(title, Text)
    assert "Dasshh" in title.plain
    
    # Check the content is formatted as Markdown
    content = rendered.renderables[1]
    assert isinstance(content, Markdown)
    assert content.markup == "Hello, I'm the assistant!"


def test_chat_message_empty_assistant():
    """Test rendering an empty assistant message (typing indicator)."""
    message = ChatMessage(
        invocation_id="test_id",
        role="assistant",
        content=""
    )
    
    # Temporarily set the role to "assistant" for the test
    # The role was previously set to "dasshh" in __init__
    message.role = "assistant"
    
    rendered = message.render()
    
    # Check that the rendered output is a Text object (typing indicator)
    assert isinstance(rendered, Text)
    assert "typing..." in rendered.plain
    assert "italic dim" in rendered.style 