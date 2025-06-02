from textual.app import ComposeResult
from textual.widgets import Static, Input, Select
from textual.reactive import reactive
from textual.validation import Regex
from textual import on

from .settings_section import SettingsSection
from .checkbox import Checkbox
from dasshh.core.logging import get_logger

logger = get_logger(__name__)


class DasshhConfig(SettingsSection):
    """Dasshh Configuration section component."""

    skip_summarization: reactive[bool] = reactive(False)
    system_prompt: reactive[str] = reactive("")
    tool_directories: reactive[str] = reactive("")

    def __init__(self, **kwargs):
        super().__init__("Dasshh Configuration", **kwargs)

    @property
    def config(self) -> dict:
        return self.app.config

    def compose(self) -> ComposeResult:
        yield from super().compose()

        yield Checkbox(id="skip-summarization", label="Skip Summarization")

        yield Static("System Prompt:")
        yield Input(placeholder="Custom system prompt...", id="system-prompt", valid_empty=True)

        yield Static("Theme:")
        yield Select([("lime", "lime")], prompt="Select theme", id="theme", allow_blank=False)

        yield Static("Tool Directories:")
        yield Input(
            placeholder="Comma-separated paths (e.g., /path/to/tool1,/path/to/tool2)",
            id="tool-directories",
            type="text",
            validators=[
                Regex(
                    r"^[a-zA-Z0-9/_-]+(,[a-zA-Z0-9/_-]+)*$",
                    failure_description="Tool directories must be valid comma-separated paths",
                )
            ],
            valid_empty=True
        )

        yield Static("Selected Model:")
        yield Select([], prompt="Select model", id="model")

    def on_mount(self) -> None:
        """Load current configuration when the widget mounts."""
        self._load_config()
        self._update_ui()

    def _load_config(self):
        try:
            dasshh_config = self.app.config

            self.skip_summarization = dasshh_config.get("skip_summarization", False)
            self.system_prompt = dasshh_config.get("system_prompt", None)
            tool_dirs = dasshh_config.get("tool_directories", [])
            self.tool_directories = ",".join(tool_dirs) if tool_dirs else None
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

            model_select = self.query_one("#model")
            model_select.set_options((model, model) for model in self.app.available_models if model)
            if self.app.selected_model:
                model_select.value = self.app.selected_model
        except Exception as e:
            logger.error(f"Error updating UI: {e}")
            self.notify(f"Error updating UI: {e}", severity="error", timeout=5)

    # -- event handlers --

    @on(Checkbox.Changed, "#skip-summarization")
    def on_skip_summarization_changed(self, event: Checkbox.Changed) -> None:
        self.skip_summarization = True if event.value else False
        self.config["dasshh"]["skip_summarization"] = self.skip_summarization
        self.app.runtime.skip_summarization = self.skip_summarization
        self.app.update_config()

    @on(Input.Changed, "#system-prompt")
    def on_system_prompt_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.system_prompt = event.value
            self.config["dasshh"]["system_prompt"] = self.system_prompt
            self.app.runtime.system_prompt = self.system_prompt
            self.app.update_config()

    @on(Select.Changed, "#theme")
    def on_theme_changed(self, event: Select.Changed) -> None:
        self.app.theme = event.value

    @on(Select.Changed, "#model")
    def on_model_changed(self, event: Select.Changed) -> None:
        if event.value == Select.BLANK:
            self.app.selected_model = None
        else:
            self.app.selected_model = event.value

    @on(Input.Changed, "#tool-directories")
    def on_tool_directories_changed(self, event: Input.Changed) -> None:
        if event.validation_result.is_valid:
            self.tool_directories = event.value if event.value else None
            self.config["dasshh"]["tool_directories"] = [d.strip() for d in event.value.split(",") if d.strip()]
            self.app.update_config()
        else:
            failure_descriptions = "\n".join(event.validation_result.failure_descriptions)
            self.notify(failure_descriptions, severity="error", timeout=5)
