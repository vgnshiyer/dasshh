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
                "I created Dasshh 🗲  because I wanted a personal assistant right in my terminal - "
                "a place where I already spend most of my time.\n\n"
                "I needed something to reduce my cognitive load - a tool that would handle these things "
                "while letting me focus on what matters.\n\n"
                "The Goal: Create a tool that will help me get things done with lesser brain juice.\n\n"
                "All through simple, conversational interaction in the terminal (Prompt to Action).\n\n"
                "Note: This is still a work in progress, but it's already making my digital life more manageable. "
                "I hope it helps you too.\n\n"
                "Star this project: https://github.com/vgnshiyer/dasshh",
            )
