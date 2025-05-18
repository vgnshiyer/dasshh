from typing import List

from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from rich.text import Text
from litellm.types.utils import Message

from dasshh.ui.components.chat.message import ChatMessage
from dasshh.ui.components.chat.chat_input import ChatInput


class ChatPanel(Widget):
    """Main chat panel containing the chat history and input area."""

    DEFAULT_CSS = """
    ChatPanel {
        layout: vertical;
        border: round $secondary;

        &:focus, &:hover, &:focus-within {
            border: round $primary;
        }

        #messages-container {
            height: 1fr;
            overflow-y: auto;
        }

        #chat-header {
            height: auto;
            text-align: center;
            text-style: bold;
        }

        ScrollableContainer {
            scrollbar-color: $secondary $background;
            scrollbar-background: $background;
            scrollbar-corner-color: $background;
            scrollbar-size: 1 1;
            scrollbar-gutter: stable;
        }
    }
    """

    current_assistant_message: ChatMessage | None = None
    """Store reference to current assistant message for streaming updates."""

    def compose(self) -> ComposeResult:
        yield Static("Chat", id="chat-header")
        yield ScrollableContainer(id="messages-container")
        yield ChatInput(id="chat-input")

    def on_show(self) -> None:
        """Chat panel shown."""
        self.query_one("#messages-container").scroll_end(animate=False)

    def reset(self) -> None:
        """Reset the chat panel."""
        container = self.query_one("#messages-container")
        container.remove_children()

        text = Static(Text("Start a new session or load a previous one.", style="dim"), classes="chat-message")
        text.styles.text_align = "center"
        text.styles.margin = (1, 1, 1, 1)
        container.mount(text)
        self.current_assistant_message = None

        chat_input = self.query_one(ChatInput)
        chat_input.disable()

    def load_messages(self, messages: List[Message]) -> None:
        """Load messages from a previous chat session."""
        container = self.query_one("#messages-container")
        container.remove_children()
        for message in messages:
            self.add_new_message(message)
        chat_input = self.query_one(ChatInput)
        chat_input.enable()

    def add_new_message(self, message: Message) -> None:
        """Add a new message to the chat history."""
        container = self.query_one("#messages-container")
        message_widget = ChatMessage(
            role=message.role,
            content=message.content,
            classes="chat-message"
        )
        container.mount(message_widget)

        if message.role == "assistant":
            self.current_assistant_message = message_widget
        container.scroll_end()

    def update_assistant_message(self, *, content: str, final: bool = False) -> None:
        """Update the content of the most recent assistant message (used for streaming)."""
        if final:
            self.current_assistant_message.content = content

        if not final and self.current_assistant_message:
            self.current_assistant_message.content += content

        container = self.query_one("#messages-container")
        container.scroll_end()

    def handle_error(self, error: str) -> None:
        """Handle an error in the chat."""
        if self.current_assistant_message:
            self.current_assistant_message.content = "Sorry, I encountered an error while processing your request."

        container = self.query_one("#messages-container")
        container.scroll_end()
