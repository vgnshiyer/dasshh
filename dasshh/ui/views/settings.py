from textual.widgets import Static
from textual.app import ComposeResult
from textual.widget import Widget


class Settings(Widget):
    """Settings"""

    DEFAULT_CSS = """
    Settings {
        layout: vertical;
        height: 1fr;
        width: 1fr;
        align: center middle;
    }

    Settings > Static {
        text-align: center;
        width: 100%;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Coming soon!")
