import logging
import yaml
from textual.reactive import reactive
from textual.app import App
from textual.command import CommandPalette
from textual.theme import ThemeProvider

from dasshh.ui.screens.main import MainScreen
from dasshh.data.client import DBClient
from dasshh.data.session import SessionService
from dasshh.core.runtime import DasshhRuntime
from dasshh.ui.utils import load_tools, load_config
from dasshh.ui.constants import DEFAULT_CONFIG_PATH
from dasshh.ui.themes.lime import lime
from dasshh.ui.model_provider import ModelProvider


class Dasshh(App):
    """Dasshh 🗲"""

    SCREENS = {
        "main": MainScreen,
    }

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+t", "toggle_theme", "Toggle Theme"),
        ("ctrl+p", "select_model", "Select Model"),
    ]

    ENABLE_COMMAND_PALETTE = False

    logger: logging.Logger
    """Dasshh logger."""

    runtime: DasshhRuntime
    """Dasshh runtime."""

    session_service: SessionService = SessionService(DBClient())
    """The database service."""

    config: dict
    """Dasshh config."""

    selected_model: reactive[str] = reactive("")
    """The selected model for the runtime."""

    available_models: reactive[list[str]] = reactive([])
    """The available models for the runtime."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("dasshh.app")
        self.logger.debug("-- Dasshh 🗲 initialized --")

        self.config = load_config()
        self.selected_model = self.get_from_config("dasshh.selected_model")
        self.available_models = [model["model_name"] for model in self.get_from_config("models")]
        load_tools(self.get_from_config("dasshh.tool_directories"))

        self._configure_runtime()

    def _configure_runtime(self):
        """Configure the runtime."""
        self.runtime = DasshhRuntime(
            session_service=self.session_service,
            model_config=self.get_model_config(self.selected_model),
            system_prompt=self.get_from_config("dasshh.system_prompt"),
            skip_summarization=self.get_from_config("dasshh.skip_summarization"),
        )

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

    def action_select_model(self) -> None:
        self.push_screen(
            CommandPalette(
                providers=[ModelProvider],
                placeholder="Search for models…",
            ),
        )

    def watch_theme(self, theme: str) -> None:
        self.config["dasshh"]["theme"] = theme
        self.update_config()

    def watch_selected_model(self, model: str) -> None:
        self.selected_model = model
        if hasattr(self, "runtime"):
            self.runtime.model_config = self.get_model_config(model)
        self.config["dasshh"]["selected_model"] = model
        self.update_config()

    def update_config(self) -> None:
        self.logger.debug(f"Updating config: {self.config}")
        DEFAULT_CONFIG_PATH.write_text(yaml.dump(self.config))

    def get_from_config(self, key: str) -> dict | str | list | None:
        """Get a value from the configuration file."""
        if not self.config:
            return None

        if "." in key:
            parts = key.split(".")
            curr = self.config
            for part in parts:
                if curr is None or part not in curr:
                    return None
                curr = curr.get(part)
            return curr

        return self.config.get(key, None)

    def get_model_config(self, model_name: str) -> dict | None:
        """Get the model configuration for a given model name."""
        for model in self.get_from_config("models"):
            if model["model_name"] == model_name:
                return model
        return None


if __name__ == "__main__":
    app = Dasshh()
    app.run()
