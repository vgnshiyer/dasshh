import logging
from textual.app import App

from dasshh.ui.screens.main import MainScreen
from dasshh.data.client import DBClient


class Dasshh(App):
    """Dasshh 🗲"""

    SCREENS = {
        "main": MainScreen,
    }

    BINDINGS = [
        ("ctrl+c", "quit", "Quit")
    ]

    db_client: DBClient
    """The database client."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = DBClient()

        self.logger = logging.getLogger("dasshh.app")
        self.logger.debug("-- Dasshh 🗲 initialized --")

    async def on_mount(self):
        self.theme = "dracula"
        self.logger.debug("Pushing main screen")
        self.push_screen("main")

    async def on_unmount(self):
        self.logger.debug("Application shutting down")


if __name__ == "__main__":
    app = Dasshh()
    app.run()
