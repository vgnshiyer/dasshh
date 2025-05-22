from textual.app import ComposeResult
from textual.widgets import Static
from textual.widget import Widget
from textual.containers import ScrollableContainer


class About(Widget):
    """About"""

    DEFAULT_CSS = """
    About {
        layout: vertical;
        height: 1fr;
        width: 1fr;
        align: center middle;
        padding: 2 4;
    }

    .about-content {
        text-align: center;
        content-align: center middle;
        padding: 1;
        width: 90%;
        max-width: 100;
    }
    """

    def compose(self) -> ComposeResult:
        with ScrollableContainer(classes="about-content"):
            yield Static(
                "Dasshh 🗲  is your friendly assistant built right into the terminal - "
                "where you spend most of your time.\n\n"
                "Designed to reduce cognitive load, Dasshh handles repetitive tasks "
                "on your behalf so that you can focus on what truly matters.\n\n"
                "The Goal: Prompt to Action!\n\n"
                "Note: This project is under active development. Contributions are welcome!\n\n"
                "Star it to show your support: https://github.com/vgnshiyer/dasshh",
            )
