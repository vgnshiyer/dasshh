import logging
import yaml
from textual.app import App
from textual.command import CommandPalette
from textual.theme import ThemeProvider

from dasshh.ui.screens.main import MainScreen
from dasshh.data.client import DBClient
from dasshh.data.session import SessionService
from dasshh.core.runtime import DasshhRuntime
from dasshh.ui.utils import load_tools, load_config, DEFAULT_CONFIG_PATH
from dasshh.ui.themes.lime import lime


class Dasshh(App):
    """Dasshh 🗲"""

    SCREENS = {
        "main": MainScreen,
    }

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+t", "toggle_theme", "Toggle Theme"),
    ]

    ENABLE_COMMAND_PALETTE = False

    logger: logging.Logger
    """Dasshh logger."""

    runtime: DasshhRuntime
    """Dasshh runtime."""

    session_service: SessionService
    """The database service."""

    config: dict
    """Dasshh config."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()
        load_tools()

        self.session_service = SessionService(DBClient())
        self.runtime = DasshhRuntime(self.session_service)

        self.logger = logging.getLogger("dasshh.app")
        self.logger.debug("-- Dasshh 🗲 initialized --")

    async def on_mount(self):
        self.startup()
        self.logger.debug("Pushing main screen")
        self.push_screen("main")
        await self.runtime.start()

    async def on_unmount(self):
        self.logger.debug("Application shutting down")
        await self.runtime.stop()

    def startup(self):
        self.register_theme(lime)
        self.theme = self.config.get("dasshh", {}).get("theme", "lime")
        self.logger.debug(f"Theme set to {self.theme}")

    def action_toggle_theme(self) -> None:
        self.push_screen(
            CommandPalette(
                providers=[ThemeProvider],
                placeholder="Search for themes…",
            ),
        )

    def watch_theme(self, theme: str) -> None:
        self.config["dasshh"]["theme"] = theme
        self.update_config()

    def update_config(self) -> None:
        self.logger.debug(f"Updating config: {self.config}")
        DEFAULT_CONFIG_PATH.write_text(yaml.dump(self.config))


if __name__ == "__main__":
    app = Dasshh()
    app.run()
