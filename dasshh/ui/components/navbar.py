from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Static

from dasshh.ui.events import ChangeView


class NavItem(Static):
    """A navigation item."""

    DEFAULT_CSS = """
    NavItem {
        content-align: center middle;
        width: auto;
        height: auto;
        padding: 0 2;
        color: $text-muted;
    }

    NavItem:hover {
        color: $primary-lighten-1;
    }

    NavItem.active {
        color: $primary-lighten-1;
        text-style: bold;
    }
    """

    def __init__(self, route: str, label: str, icon: str = "", **kwargs):
        super().__init__(f"{icon} {label}", **kwargs)
        self.route = route

    def on_click(self) -> None:
        self.add_class("active")
        self.post_message(ChangeView(self.route))


class Logo(Static):
    """The logo."""

    DEFAULT_CSS = """
    Logo {
        color: $primary;
        content-align: center middle;
        text-style: italic bold;
        width: auto;
        height: 100%;
        margin-top: -1;
    }

    Logo:hover {
        color: $primary-darken-1;
    }
    """

    txt = """
    ╭──────────╮
    │ Dasshh 🗲 │
    ╰──────────╯
    """

    def render(self) -> str:
        return self.txt


class Navbar(Container):
    """The Navbar"""

    DEFAULT_CSS = """
    Navbar {
        content-align: center middle;
        layout: horizontal;
        background: $background-lighten-1;
        width: 100%;
        height: 3;
    }

    Navbar > #logo {
        width: 1fr;
        align: right middle;
    }

    Navbar > #nav-items {
        width: 1fr;
        align: left middle;
    }
    """

    def compose(self) -> ComposeResult:
        """Create the navbar items."""
        yield Logo(id="logo")
        with Horizontal(id="nav-items"):
            yield NavItem(route="chat", label="Chat", icon="󰭹", id="chat")
            yield NavItem(route="settings", label="Settings", icon="", id="settings")
            yield NavItem(route="about", label="About", icon="", id="about")

    def on_mount(self) -> None:
        self.query_one("#chat").add_class("active")

    @on(ChangeView)
    def change_view(self, event: ChangeView):
        for item in self.query("NavItem"):
            item.remove_class("active")
        self.query_one(f"#{event.view}").add_class("active")
