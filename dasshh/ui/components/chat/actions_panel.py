from typing import List
from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from litellm.types.utils import ChatCompletionMessageToolCall, Message

from dasshh.ui.components.chat.action import Action, ActionResult


class ActionsPanel(Widget):
    DEFAULT_CSS = """
    ActionsPanel {
        border: round $secondary;
        layout: vertical;

        &:focus, &:hover, &:focus-within {
            border: round $primary;
        }

        #actions-header {
            height: auto;
            text-align: center;
            text-style: bold;
        }

        #actions-container {
            height: 1fr;
            margin: 1;
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

    def compose(self) -> ComposeResult:
        yield Static("Actions", id="actions-header")
        yield ScrollableContainer(id="actions-container")

    def on_show(self) -> None:
        """Actions panel shown."""
        self.query_one("#actions-container").scroll_end(animate=False)

    def reset(self) -> None:
        """Reset the actions panel."""
        container = self.query_one("#actions-container")
        container.remove_children()

    def load_actions(self, actions: List[ChatCompletionMessageToolCall | Message]):
        container = self.query_one("#actions-container", ScrollableContainer)
        container.remove_children()
        for action in actions:
            self.add_action(action)

    def add_action(self, action: ChatCompletionMessageToolCall | Message) -> None:
        """Add a action to the actions panel."""
        container = self.query_one("#actions-container", ScrollableContainer)
        if isinstance(action, ChatCompletionMessageToolCall):
            action_widget = Action(
                name=action.function.name,
                args=action.function.arguments,
            )
            container.mount(action_widget)
        elif isinstance(action, Message) and action.role == "tool":
            action_widget = ActionResult(
                name=action.name,
                result=action.content,
            )
            container.mount(action_widget)
        container.scroll_end()

    def handle_error(self, error: str) -> None:
        """Handle an error during an action by showing a toast notification."""
        self.notify(f"Tool Error: {error}", severity="error", timeout=5)
