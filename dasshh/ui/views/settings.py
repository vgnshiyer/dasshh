from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import ScrollableContainer

from dasshh.core.logging import get_logger
from dasshh.ui.components.settings import DasshhConfig, ModelsList

logger = get_logger(__name__)


class Settings(Widget):
    """Settings view with all configuration options."""

    DEFAULT_CSS = """
    Settings {
        layout: vertical;
        height: 1fr;
        width: 80%;
    }

    Settings > ScrollableContainer {
        height: 1fr;
        width: 100%;
        scrollbar-color: $secondary $background;
        scrollbar-background: $background;
        scrollbar-corner-color: $background;
        scrollbar-size: 1 1;
        scrollbar-gutter: stable;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="settings-container"):
            yield DasshhConfig()
            yield ModelsList()
