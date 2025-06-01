from textual.reactive import reactive
from textual.widgets import Input
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import ScrollableContainer

from dasshh.core.logging import get_logger
from dasshh.ui.components.settings import DasshhConfig, ModelConfig, Checkbox

logger = get_logger(__name__)


class Settings(Widget):
    """Settings view with all configuration options."""

    skip_summarization = reactive(False)
    system_prompt = reactive("")
    tool_directories = reactive("")
    model_name = reactive("")
    api_base = reactive("")
    api_key = reactive("")
    api_version = reactive("")
    temperature = reactive(1.0)
    top_p = reactive(1.0)
    max_tokens = reactive(None)
    max_completion_tokens = reactive(None)

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
        self.config = self.app.config

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="settings-container"):
            yield DasshhConfig()
            yield ModelConfig()

    def on_mount(self) -> None:
        """Load current configuration when the widget mounts."""
        self._load_config()
        self._update_ui()

    def _load_config(self) -> None:
        """Load the current configuration and populate the form fields."""
        try:
            dasshh_config = self.config.get("dasshh", {})

            self.skip_summarization = dasshh_config.get("skip_summarization", False)
            self.system_prompt = dasshh_config.get("system_prompt", None)
            tool_dirs = dasshh_config.get("tool_directories", [])
            self.tool_directories = ",".join(tool_dirs) if tool_dirs else None

            model_config = self.config.get("model", {})
            self.model_name = model_config.get("name", None)
            self.api_base = model_config.get("api_base", None)
            self.api_key = model_config.get("api_key", None)
            self.api_version = model_config.get("api_version", None)
            self.temperature = model_config.get("temperature", 1.0)
            self.top_p = model_config.get("top_p", 1.0)
            self.max_tokens = model_config.get("max_tokens", None)
            self.max_completion_tokens = model_config.get("max_completion_tokens", None)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            self.notify(f"Error loading config: {str(e)}", severity="error", timeout=5)

    def _update_ui(self) -> None:
        """Update UI elements from reactive values."""
        try:
            skip_sum_checkbox = self.query_one("#skip-summarization", Checkbox)
            skip_sum_checkbox.value = self.skip_summarization

            system_prompt_input = self.query_one("#system-prompt", Input)
            system_prompt_input.value = self.system_prompt or ""

            theme_select = self.query_one("#theme")
            theme_select.set_options((theme, theme) for theme in self.app.available_themes.keys())
            theme_select.value = self.app.theme

            tool_dirs_input = self.query_one("#tool-directories", Input)
            tool_dirs_input.value = self.tool_directories or ""

            model_name_input = self.query_one("#model-name", Input)
            model_name_input.value = self.model_name or ""

            api_base_input = self.query_one("#api-base", Input)
            api_base_input.value = self.api_base or ""

            api_key_input = self.query_one("#api-key", Input)
            api_key_input.value = self.api_key or ""

            api_version_input = self.query_one("#api-version", Input)
            api_version_input.value = self.api_version or ""

            temperature_input = self.query_one("#temperature", Input)
            temperature_input.value = str(self.temperature) or ""

            top_p_input = self.query_one("#top-p", Input)
            top_p_input.value = str(self.top_p) or ""

            max_tokens_input = self.query_one("#max-tokens", Input)
            max_tokens_input.value = str(self.max_tokens) if self.max_tokens else ""

            max_completion_tokens_input = self.query_one("#max-completion-tokens", Input)
            max_completion_tokens_input.value = str(self.max_completion_tokens) if self.max_completion_tokens else ""
        except Exception as e:
            logger.error(f"Error updating UI: {e}")
            self.notify(f"Error updating UI: {e}", severity="error", timeout=5)

    # -- watch methods --

    def watch_skip_summarization(self, value: bool) -> None:
        self.config["dasshh"]["skip_summarization"] = value
        self.app.update_config()
        self.app.runtime.skip_summarization = value

    def watch_system_prompt(self, value: str) -> None:
        self.config["dasshh"]["system_prompt"] = value
        self.app.update_config()
        if value:
            self.app.runtime.system_prompt = value

    def watch_tool_directories(self, value: str) -> None:
        self.config["dasshh"]["tool_directories"] = [d.strip() for d in value.split(",") if d.strip()]
        self.app.update_config()

    def watch_model_name(self, value: str) -> None:
        self.config["model"]["name"] = value
        self.app.update_config()
        if value:
            self.app.runtime.model = value

    def watch_api_base(self, value: str) -> None:
        self.config["model"]["api_base"] = value
        self.app.update_config()
        if value:
            self.app.runtime.api_base = value

    def watch_api_key(self, value: str) -> None:
        self.config["model"]["api_key"] = value
        self.app.update_config()
        if value:
            self.app.runtime.api_key = value

    def watch_api_version(self, value: str) -> None:
        self.config["model"]["api_version"] = value
        self.app.update_config()
        if value:
            self.app.runtime.api_version = value

    def watch_temperature(self, value: float) -> None:
        self.config["model"]["temperature"] = value
        self.app.update_config()
        if value:
            self.app.runtime.temperature = value

    def watch_top_p(self, value: float) -> None:
        self.config["model"]["top_p"] = value
        self.app.update_config()
        if value:
            self.app.runtime.top_p = value

    def watch_max_tokens(self, value) -> None:
        self.config["model"]["max_tokens"] = value
        self.app.update_config()
        if value:
            self.app.runtime.max_tokens = value

    def watch_max_completion_tokens(self, value) -> None:
        self.config["model"]["max_completion_tokens"] = value
        self.app.update_config()
        if value:
            self.app.runtime.max_completion_tokens = value
