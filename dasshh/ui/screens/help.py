from textual.widgets import Static
from textual.app import ComposeResult
from textual.widget import Widget


class Help(Widget):
    def compose(self) -> ComposeResult:
        yield Static("Help")
