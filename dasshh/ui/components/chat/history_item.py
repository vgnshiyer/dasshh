from datetime import datetime, timezone
from typing import Any

from textual.widgets import Static
from textual.reactive import reactive
from rich.console import Group
from rich.text import Text

from dasshh.ui.events import LoadSession, DeleteSession


class DeleteIcon(Static):
    """A static widget that displays a delete icon."""

    DEFAULT_CSS = """
    DeleteIcon {
        padding: 0 1;
        color: $text-muted;
        align: center middle;
        text-align: center;

        &:hover {
            color: $error;
        }
    }
    """

    selected: reactive[bool] = reactive(False, layout=True)

    def __init__(self, session_id: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.session_id = session_id

    def watch_selected(self, selected: bool) -> None:
        """Watch for changes to the selected state."""
        if selected:
            self.add_class("selected")
        else:
            self.remove_class("selected")

    def on_click(self) -> None:
        """Handle click events on this widget."""
        self.post_message(DeleteSession(self.session_id))

    def render(self):
        return Text("󰆴 Delete")


class HistoryItem(Static):
    """A history item display component for chat sessions."""

    DEFAULT_CSS = """
    HistoryItem {
        margin-top: 1;
        padding: 1;

    }
    """

    detail: reactive[str] = reactive("", layout=True)
    selected: reactive[bool] = reactive(False, layout=True)

    def __init__(
        self,
        session_id: str,
        detail: str,
        created_at: datetime,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.session_id = session_id
        self.detail = detail
        self.created_at = created_at

    def watch_selected(self, selected: bool) -> None:
        """Watch for changes to the selected state."""
        if selected:
            self.add_class("selected")
        else:
            self.remove_class("selected")

    def on_click(self) -> None:
        """Handle click events on this widget."""
        self.post_message(LoadSession(self.session_id))

    def render(self):
        truncated_detail = (
            (self.detail[:40] + "...") if len(self.detail) > 40 else self.detail
        )

        local_timestamp = self.created_at.replace(tzinfo=timezone.utc).astimezone(
            tz=None
        )

        now = datetime.now()
        time_str = local_timestamp.strftime("%I:%M %p")

        if local_timestamp.date() == now.date():
            date_str = f"Today at {time_str}"
        elif (now.date() - local_timestamp.date()).days == 1:
            date_str = f"Yesterday at {time_str}"
        else:
            date_str = local_timestamp.strftime("%b %d at %I:%M %p")

        title = Text(truncated_detail, style="bold")
        date = Text(date_str, style="dim")

        return Group(title, date)
