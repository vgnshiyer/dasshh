import logging
from textual.app import App

from dasshh.ui.screens.main import MainScreen
from dasshh.data.client import DBClient
from dasshh.data.session import SessionService
from dasshh.core.runtime import DasshhRuntime


class Dasshh(App):
    """Dasshh 🗲"""

    SCREENS = {
        "main": MainScreen,
    }

    BINDINGS = [
        ("ctrl+c", "quit", "Quit")
    ]

    logger: logging.Logger
    """Dasshh logger."""

    runtime: DasshhRuntime
    """Dasshh runtime."""

    session_service: SessionService
    """The database service."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_service = SessionService(DBClient())
        self.runtime = DasshhRuntime(self.session_service)

        self.logger = logging.getLogger("dasshh.app")
        self.logger.debug("-- Dasshh 🗲 initialized --")

    async def on_mount(self):
        self.theme = "dracula"
        await self.runtime.start()
        self.logger.debug("Pushing main screen")
        self.push_screen("main")

    async def on_unmount(self):
        self.logger.debug("Application shutting down")
        await self.runtime.stop()


if __name__ == "__main__":
    app = Dasshh()
    app.run()
