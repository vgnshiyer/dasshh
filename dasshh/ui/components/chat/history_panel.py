from typing import List

from textual.widget import Widget
from textual.widgets import Static, Button
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual import on

from dasshh.ui.events import NewSession, DeleteSession
from dasshh.ui.components.chat.history_item import HistoryItem, DeleteIcon
from dasshh.ui.types import UISession


class HistoryPanel(Widget):
    DEFAULT_CSS = """
    HistoryPanel {
        border: round $secondary;
        layout: vertical;

        &:focus, &:hover, &:focus-within {
            border: round $primary;
        }

        #history-header {
            height: auto;
            text-align: center;
            text-style: bold;
        }

        #history-container {
            height: 1fr;
            margin: 1;
        }

        #new-session {
            width: 100%;
            min-width: 10;
            border: round $secondary;
            color: $secondary;
            background: $background;
            text-style: bold;
        }

        #new-session:focus, #new-session:hover {
            border: round $primary;
            color: $primary;
            background: $background;
            background-tint: $background;
            text-style: bold;

            &.-active {
                tint: $background;
            }
        }

        ScrollableContainer {
            scrollbar-color: $secondary $background;
            scrollbar-background: $background;
            scrollbar-corner-color: $background;
            scrollbar-size: 1 1;
            scrollbar-gutter: stable;
        }

        HistoryItem, DeleteIcon {
            width: 100%;
            height: auto;
            border-left: thick $accent-darken-2;
            background: $panel-darken-1;

            &:hover {
                border-left: thick $accent;
                background: $panel 20%;
            }

            &.selected {
                border-left: thick $success;
                background: $panel-lighten-1;
            }
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Sessions", id="history-header")
        yield ScrollableContainer(id="history-container")
        yield Button("New Session", id="new-session")

    def on_show(self) -> None:
        """History panel shown."""
        self.query_one("#history-container").scroll_end(animate=False)

    @on(Button.Pressed, "#new-session")
    def on_button_pressed(self) -> None:
        """Handle button presses."""
        self.post_message(NewSession())

    @on(DeleteSession)
    def on_delete_session(self, event: DeleteSession) -> None:
        """Handle session deletion request."""
        item = self.get_history_item_widget(event.session_id)
        if item:
            item.remove()

        container = self.query_one("#history-container", ScrollableContainer)
        for item in container.query(DeleteIcon):
            if item.session_id == event.session_id:
                item.remove()
                break

    def load_sessions(self, sessions: List[UISession], current: str) -> None:
        """Load session history from a list of sessions."""
        container = self.query_one("#history-container", ScrollableContainer)
        container.remove_children()

        for session in sessions:
            history_item = HistoryItem(
                session_id=session.id,
                detail=session.detail,
                created_at=session.updated_at,
            )
            delete_icon = DeleteIcon(session_id=session.id)
            # Mark current session
            if session.id == current:
                history_item.selected = True
                delete_icon.selected = True
            container.mount(history_item, delete_icon)
        container.scroll_end()

    def add_session(self, session: UISession) -> None:
        """Add a session to the history panel."""
        container = self.query_one("#history-container", ScrollableContainer)
        history_item = HistoryItem(
            session_id=session.id,
            detail=session.detail,
            created_at=session.updated_at,
        )
        delete_icon = DeleteIcon(session_id=session.id)
        container.mount(history_item, delete_icon)
        container.scroll_end()

    def set_current_session(self, session_id: str) -> None:
        """Set the current selected session."""
        # Update selected state for all items
        container = self.query_one("#history-container", ScrollableContainer)
        for item in container.query(HistoryItem):
            item.selected = item.session_id == session_id
        for item in container.query(DeleteIcon):
            item.selected = item.session_id == session_id

    def get_history_item_widget(self, session_id: str) -> HistoryItem | None:
        """Get a history item widget by session id."""
        container = self.query_one("#history-container", ScrollableContainer)
        for item in container.query(HistoryItem):
            if item.session_id == session_id:
                return item
        return None
