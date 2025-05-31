from textual.reactive import reactive
from textual.widgets import Static, Input, Checkbox, Select, Label
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Container, ScrollableContainer
from textual.validation import Number, Regex, Function
from textual import on

from dasshh.core.logging import get_logger

logger = get_logger(__name__)


class SettingsSection(Container):
    """A section container for grouping related settings."""

    DEFAULT_CSS = """
    SettingsSection {
        layout: vertical;
        width: 100%;
        height: auto;
        padding: 1;
        border: round $panel;
        background: $panel;
    }

    SettingsSection > Label {
        text-style: bold;
        color: $primary;
        margin-bottom: 2;
        dock: top;
    }
    """

    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title)


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
        width: 1fr;
        padding: 2;
    }

    Settings > ScrollableContainer {
        height: 1fr;
        width: 100%;
    }

    Settings > #settings-header {
        height: auto;
        width: 100%;
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 2;
    }

    #status-message {
        text-align: center;
        margin-top: 1;
        color: $text;
        height: auto;
        width: 100%;
    }

    ScrollableContainer {
        scrollbar-color: $secondary $background;
        scrollbar-background: $background;
        scrollbar-corner-color: $background;
        scrollbar-size: 1 1;
        scrollbar-gutter: stable;
    }

    SettingRow > Static {
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = self.app.config

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="settings-container"):
            with SettingsSection("Dasshh Configuration"):
                yield Checkbox(id="skip-summarization", label="Skip Summarization")

                yield Static("System Prompt:")
                yield Input(placeholder="Custom system prompt...", id="system-prompt", valid_empty=True)

                yield Static("Theme:")
                yield Select([], prompt="Select theme", id="theme")

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

            with SettingsSection("Model Configuration"):
                yield Static("Model Name:")
                yield Input(
                    placeholder="e.g., gemini/gemini-2.0-flash",
                    id="model-name",
                    validators=[
                        Function(lambda value: value is not None and value.strip()),
                    ],
                    valid_empty=False
                )

                yield Static("API Base:")
                yield Input(placeholder="API base URL (optional)", id="api-base", valid_empty=True)

                yield Static("API Key:")
                yield Input(
                    placeholder="Your API key", password=True, id="api-key",
                    validators=[
                        Function(lambda value: value is not None and value.strip()),
                    ],
                    valid_empty=False
                )

                yield Static("API Version:")
                yield Input(placeholder="API version (optional)", id="api-version", valid_empty=True)

                yield Static("Temperature:")
                yield Input(
                    placeholder="0.0 - 1.0 (default: 1.0)",
                    id="temperature",
                    type="number",
                    validators=[
                        Number(
                            minimum=0.0,
                            maximum=1.0,
                            failure_description="Temperature must be a value in the range 0.0 to 1.0",
                        )
                    ],
                    valid_empty=False
                )

                yield Static("Top P:")
                yield Input(
                    placeholder="0.0 - 1.0 (default: 1.0)",
                    id="top-p",
                    type="number",
                    validators=[
                        Number(
                            minimum=0.0,
                            maximum=1.0,
                            failure_description="Top P must be a value in the range 0.0 to 1.0",
                        )
                    ],
                    valid_empty=False
                )

                yield Static("Max Tokens:")
                yield Input(
                    placeholder="Maximum tokens (optional)",
                    id="max-tokens",
                    type="integer",
                    valid_empty=True
                )

                yield Static("Max Completion Tokens:")
                yield Input(
                    placeholder="Maximum completion tokens (optional)",
                    id="max-completion-tokens",
                    type="integer",
                    valid_empty=True
                )

        yield Static("", id="status-message")

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
            status_message = self.query_one("#status-message", Static)
            status_message.update(f"Error loading config: {str(e)}")
            status_message.styles.color = "red"

    def _update_ui(self) -> None:
        """Update UI elements from reactive values."""
        try:
            skip_sum_checkbox = self.query_one("#skip-summarization", Checkbox)
            skip_sum_checkbox.value = self.skip_summarization

            system_prompt_input = self.query_one("#system-prompt", Input)
            system_prompt_input.value = self.system_prompt or ""

            theme_select = self.query_one("#theme", Select)
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
            status_message = self.query_one("#status-message", Static)
            status_message.update(f"Error updating UI: {e}")
            status_message.styles.color = "red"

    # -- watch methods --

    def watch_skip_summarization(self, value: bool) -> None:
        self.config["dasshh"]["skip_summarization"] = value
        self.app.update_config()

    def watch_system_prompt(self, value: str) -> None:
        self.config["dasshh"]["system_prompt"] = value
        self.app.update_config()

    def watch_tool_directories(self, value: str) -> None:
        self.config["dasshh"]["tool_directories"] = [d.strip() for d in value.split(",") if d.strip()]
        self.app.update_config()

    def watch_model_name(self, value: str) -> None:
        self.config["model"]["name"] = value
        self.app.update_config()

    def watch_api_base(self, value: str) -> None:
        self.config["model"]["api_base"] = value
        self.app.update_config()

    def watch_api_key(self, value: str) -> None:
        self.config["model"]["api_key"] = value
        self.app.update_config()

    def watch_api_version(self, value: str) -> None:
        self.config["model"]["api_version"] = value
        self.app.update_config()

    def watch_temperature(self, value: float) -> None:
        self.config["model"]["temperature"] = value
        self.app.update_config()

    def watch_top_p(self, value: float) -> None:
        self.config["model"]["top_p"] = value
        self.app.update_config()

    def watch_max_tokens(self, value) -> None:
        self.config["model"]["max_tokens"] = value
        self.app.update_config()

    def watch_max_completion_tokens(self, value) -> None:
        self.config["model"]["max_completion_tokens"] = value
        self.app.update_config()

    # -- Events --

    @on(Checkbox.Changed, "#skip-summarization")
    def on_skip_summarization_changed(self, event: Checkbox.Changed) -> None:
        if event.value:
            self.skip_summarization = True
        else:
            self.skip_summarization = False

    @on(Input.Changed, "#system-prompt")
    def on_system_prompt_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.system_prompt = event.value
        else:
            self.system_prompt = None

    @on(Select.Changed, "#theme")
    def on_theme_changed(self, event: Select.Changed) -> None:
        self.app.theme = event.value

    @on(Input.Changed, "#tool-directories")
    def on_tool_directories_changed(self, event: Input.Changed) -> None:
        if event.validation_result.is_valid:
            if event.value:
                self.tool_directories = event.value
            else:
                self.tool_directories = None

    @on(Input.Changed, "#model-name")
    def on_model_name_changed(self, event: Input.Changed) -> None:
        if event.validation_result.is_valid and event.value:
            self.model_name = event.value

    @on(Input.Changed, "#api-base")
    def on_api_base_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.api_base = event.value
        else:
            self.api_base = None

    @on(Input.Changed, "#api-key")
    def on_api_key_changed(self, event: Input.Changed) -> None:
        if event.validation_result.is_valid and event.value:
            self.api_key = event.value

    @on(Input.Changed, "#api-version")
    def on_api_version_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.api_version = event.value
        else:
            self.api_version = None

    @on(Input.Changed, "#temperature")
    def on_temperature_changed(self, event: Input.Changed) -> None:
        if event.validation_result.is_valid and event.value:
            self.temperature = float(event.value)

    @on(Input.Changed, "#top-p")
    def on_top_p_changed(self, event: Input.Changed) -> None:
        if event.validation_result.is_valid and event.value:
            self.top_p = float(event.value)

    @on(Input.Changed, "#max-tokens")
    def on_max_tokens_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.max_tokens = int(event.value)
        else:
            self.max_tokens = None

    @on(Input.Changed, "#max-completion-tokens")
    def on_max_completion_tokens_changed(self, event: Input.Changed) -> None:
        if event.value:
            self.max_completion_tokens = int(event.value)
        else:
            self.max_completion_tokens = None
