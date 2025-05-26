from typing import List
from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult
from textual.containers import ScrollableContainer

from dasshh.ui.components.chat.action import Action
from dasshh.ui.types import UIAction


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
        }

        ScrollableContainer {
            scrollbar-color: $secondary $background;
            scrollbar-background: $background;
            scrollbar-corner-color: $background;
            scrollbar-size: 1 1;
            scrollbar-gutter: stable;
            margin: 0 1;
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

    def load_actions(self, actions: List[UIAction]):
        container = self.query_one("#actions-container", ScrollableContainer)
        container.remove_children()
        for action in actions:
            self.add_action(action)
        container.scroll_end()

    def add_action(self, action: UIAction) -> None:
        """Add a action to the actions panel."""
        container = self.query_one("#actions-container", ScrollableContainer)
        action_widget = Action(
            invocation_id=action.invocation_id,
            tool_call_id=action.tool_call_id,
            name=action.name,
            args=action.args,
            result=action.result,
        )
        container.mount(action_widget)
        container.scroll_end()

    def update_action(self, invocation_id: str, tool_call_id: str, result: str) -> None:
        """Update an action in the actions panel."""
        action_widget = self.get_action_widget(invocation_id, tool_call_id)
        if action_widget:
            action_widget.result = result
            container = self.query_one("#actions-container", ScrollableContainer)
            container.scroll_end()

    def get_action_widget(self, invocation_id: str, tool_call_id: str) -> Action | None:
        """Get an action widget by invocation id and tool call id."""
        container = self.query_one("#actions-container", ScrollableContainer)
        for action in container.query(Action):
            if (
                action.invocation_id == invocation_id
                and action.tool_call_id == tool_call_id
            ):
                return action
        return None

    def handle_error(self, error: str) -> None:
        """Handle an error during an action by showing a toast notification."""
        self.notify(f"Tool Error: {error}", severity="error", timeout=5)
