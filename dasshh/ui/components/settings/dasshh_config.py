from textual.app import ComposeResult
from textual.widgets import Static, Input, Select
from textual.validation import Regex
from textual import on

from .settings_section import SettingsSection
from .checkbox import Checkbox


class DasshhConfig(SettingsSection):
    """Dasshh Configuration section component."""

    def __init__(self, **kwargs):
        super().__init__("Dasshh Configuration", **kwargs)

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

    @on(Checkbox.Changed, "#skip-summarization")
    def on_skip_summarization_changed(self, event: Checkbox.Changed) -> None:
        settings_widget = self.parent.parent
        if hasattr(settings_widget, 'skip_summarization'):
            settings_widget.skip_summarization = event.value

    @on(Input.Changed, "#system-prompt")
    def on_system_prompt_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if hasattr(settings_widget, 'system_prompt'):
            settings_widget.system_prompt = event.value if event.value else None

    @on(Select.Changed, "#theme")
    def on_theme_changed(self, event: Select.Changed) -> None:
        settings_widget = self.parent.parent
        if hasattr(settings_widget, 'app'):
            settings_widget.app.theme = event.value

    @on(Input.Changed, "#tool-directories")
    def on_tool_directories_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if event.validation_result.is_valid:
            if hasattr(settings_widget, 'tool_directories'):
                settings_widget.tool_directories = event.value if event.value else None
        else:
            if hasattr(settings_widget, 'notify'):
                failure_descriptions = "\n".join(event.validation_result.failure_descriptions)
                settings_widget.notify(failure_descriptions, severity="error", timeout=5)
