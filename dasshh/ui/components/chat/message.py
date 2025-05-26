from textual.reactive import reactive
from textual.widgets import Static
from rich.markdown import Markdown
from rich.console import Group
from rich.text import Text
from typing import Any


class ChatMessage(Static):
    """A chat message display component."""

    DEFAULT_CSS = """
    ChatMessage {
        width: 100%;
        margin: 1 1;
        padding: 0 1;
    }

    .user {
        border-left: thick $primary;
        background: $background-lighten-1;
        padding: 1;
        margin: 1 5 1 1;
    }

    .assistant {
        border-left: thick $accent;
        background: $background-lighten-2;
        padding: 1;
        margin: 1 1 1 5;
    }
    """
    user_icon: str = "󰀄"
    # assistant_icon: str = "󱙺"
    assistant_icon: str = "🗲"

    content: reactive[str] = reactive("", layout=True)

    def __init__(
        self, invocation_id: str, role: str, content: str, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.invocation_id = invocation_id
        if role == "user":
            self.role = "you"
        elif role == "assistant":
            self.role = "dasshh"
        self.content = content

        # Add CSS class based on role
        self.add_class(role)

    def render(self):
        # Show typing indicator if the message is from assistant but empty
        if self.role == "dasshh" and not self.content:
            return Text("typing...", style="italic dim")

        role_icon = self.user_icon if self.role == "you" else self.assistant_icon
        role_style = "bold #ffff8d" if self.role == "you" else "bold #76ff03"

        title = Text(f"{role_icon} {self.role.capitalize()}", style=role_style)
        text = Markdown(self.content) if self.content else Text("")

        return Group(title, text)
