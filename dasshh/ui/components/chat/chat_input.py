from textual.widgets import Input, Button
from textual.widget import Widget
from textual.app import ComposeResult
from textual import on
from textual.binding import Binding
from textual.containers import Horizontal

from dasshh.ui.events import NewMessage


class ChatInput(Widget):
    """Input area for chat messages."""

    BINDINGS = [Binding("escape", "blur_input", "Blur Input")]

    DEFAULT_CSS = """
    ChatInput {
        dock: bottom;
        width: 100%;
        height: 3;
        text-overflow: ellipsis;

        ScrollView {
            overflow-y: hidden;
            overflow-x: hidden;
        }
    }

    #message-input {
        width: 1fr;
        border: round $secondary;
        background: $background;

        &:focus, &:hover {
            border: round $primary;
            background: $background;
            background-tint: $background;
        }

        &:disabled {
            border: round $panel-darken-1;
            color: $text-muted;
        }
    }

    #send-button {
        width: auto;
        min-width: 10;
        border: round $secondary;
        color: $secondary;
        background: $background;
        text-style: bold;

        &:disabled {
            border: round $panel-darken-1;
            color: $text-muted;
        }
    }

    #send-button:focus, #send-button:hover {
        border: round $primary;
        color: $primary;
        background: $background;
        background-tint: $background;
        text-style: bold;

        &.-active {
            tint: $background;
        }
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Input(placeholder="Type your message here...", id="message-input")
            yield Button("Send", id="send-button", variant="primary")

    @on(Input.Submitted)
    def on_input_submitted(self) -> None:
        """Handle when the user presses Enter in the input field."""
        self.send_message()

    @on(Button.Pressed, "#send-button")
    def on_button_pressed(self) -> None:
        """Handle when the send button is clicked."""
        self.send_message()

    def action_blur_input(self) -> None:
        """Remove focus from the input field when Escape is pressed."""
        self.screen.set_focus(None)

    def send_message(self) -> None:
        """Send the message from the input field."""
        input_field = self.query_one("#message-input", Input)
        message = input_field.value

        if message.strip():
            input_field.value = ""
            self.post_message(NewMessage(message=message))

    def disable(self) -> None:
        """Disable the input field and send button."""
        input_field = self.query_one("#message-input", Input)
        send_button = self.query_one("#send-button", Button)

        input_field.disabled = True
        send_button.disabled = True

    def enable(self) -> None:
        """Enable the input field and send button."""
        input_field = self.query_one("#message-input", Input)
        send_button = self.query_one("#send-button", Button)

        input_field.disabled = False
        send_button.disabled = False
