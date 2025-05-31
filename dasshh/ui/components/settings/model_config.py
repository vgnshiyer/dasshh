from textual.app import ComposeResult
from textual.widgets import Static, Input
from textual.validation import Number, Function
from textual import on

from .settings_section import SettingsSection


class ModelConfig(SettingsSection):
    """Model Configuration section component."""

    def __init__(self, **kwargs):
        super().__init__("Model Configuration", **kwargs)

    def compose(self) -> ComposeResult:
        yield from super().compose()

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

    @on(Input.Changed, "#model-name")
    def on_model_name_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if event.validation_result.is_valid and event.value:
            if hasattr(settings_widget, 'model_name'):
                settings_widget.model_name = event.value

        if not event.validation_result.is_valid:
            if hasattr(settings_widget, 'notify'):
                settings_widget.notify("Model name is required", severity="error", timeout=5)

    @on(Input.Changed, "#api-base")
    def on_api_base_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if hasattr(settings_widget, 'api_base'):
            settings_widget.api_base = event.value if event.value else None

    @on(Input.Changed, "#api-key")
    def on_api_key_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if event.validation_result.is_valid and event.value:
            if hasattr(settings_widget, 'api_key'):
                settings_widget.api_key = event.value

        if not event.validation_result.is_valid:
            if hasattr(settings_widget, 'notify'):
                settings_widget.notify("API key is required", severity="error", timeout=5)

    @on(Input.Changed, "#api-version")
    def on_api_version_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if hasattr(settings_widget, 'api_version'):
            settings_widget.api_version = event.value if event.value else None

    @on(Input.Changed, "#temperature")
    def on_temperature_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if event.validation_result.is_valid and event.value:
            if hasattr(settings_widget, 'temperature'):
                settings_widget.temperature = float(event.value)

        if not event.validation_result.is_valid:
            if hasattr(settings_widget, 'notify'):
                settings_widget.notify(
                    "Temperature must be a value in the range 0.0 to 1.0", 
                    severity="error", 
                    timeout=5
                )

    @on(Input.Changed, "#top-p")
    def on_top_p_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if event.validation_result.is_valid and event.value:
            if hasattr(settings_widget, 'top_p'):
                settings_widget.top_p = float(event.value)

        if not event.validation_result.is_valid:
            if hasattr(settings_widget, 'notify'):
                settings_widget.notify(
                    "Top P must be a value in the range 0.0 to 1.0", 
                    severity="error", 
                    timeout=5
                )

    @on(Input.Changed, "#max-tokens")
    def on_max_tokens_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if hasattr(settings_widget, 'max_tokens'):
            settings_widget.max_tokens = int(event.value) if event.value else None

    @on(Input.Changed, "#max-completion-tokens")
    def on_max_completion_tokens_changed(self, event: Input.Changed) -> None:
        settings_widget = self.parent.parent
        if hasattr(settings_widget, 'max_completion_tokens'):
            settings_widget.max_completion_tokens = int(event.value) if event.value else None
