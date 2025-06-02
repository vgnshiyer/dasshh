import yaml

from textual.app import ComposeResult
from textual.widgets import TextArea, Button, Label
from textual.widget import Widget
from textual.reactive import reactive
from textual.containers import ScrollableContainer, Horizontal
from textual import on

from dasshh.core.logging import get_logger
from .settings_section import SettingsSection

logger = get_logger(__name__)


class ModelConfig(Widget):
    """Model Configuration"""

    DEFAULT_CSS = """
    ModelConfig {
        layout: vertical;
        padding: 1;
        margin: 1 0;
        border: round $secondary;
    }

    .model-header {
        layout: horizontal;
        height: auto;
        align: left middle;
        margin-bottom: 1;
    }

    .model-label {
        width: 1fr;
        text-style: bold;
        color: $primary;
    }

    #save-button {
        width: auto;
        min-width: 8;
        border: round $secondary;
        color: $secondary;
        background: $background;
        text-style: bold;
    }

    #save-button:focus, #save-button:hover {
        border: round $primary;
        color: $primary;
        background: $background;
        background-tint: $background;
        text-style: bold;

        &.-active {
            tint: $background;
        }
    }

    TextArea {
        border: round $secondary;
        background: $background;

        &:focus {
            border: round $primary;
        }

        scrollbar-color: $secondary $background;
        scrollbar-background: $background;
        scrollbar-corner-color: $background;
        scrollbar-size: 1 1;
        scrollbar-gutter: stable;
    }
    """

    model_name: str
    """Model identifier"""

    litellm_params: reactive[str] = reactive("")
    """Model params"""

    def __init__(self, model_name: str, litellm_params: dict, *a, **kw):
        super().__init__(*a, **kw)
        self.model_name = model_name
        self.litellm_params = yaml.dump(litellm_params)

    @property
    def config(self) -> dict:
        return self.app.config

    def compose(self) -> ComposeResult:
        with Horizontal(classes="model-header"):
            yield Label(f"Model: {self.model_name}", classes="model-label")
            yield Button("Save", id="save-button")
        yield TextArea.code_editor(self.litellm_params, language="yaml")

    def _is_valid_yaml(self, yaml_text: str) -> bool:
        try:
            yaml.safe_load(yaml_text)
            return True
        except yaml.YAMLError:
            return False

    @on(Button.Pressed, "#save-button")
    def on_config_change(self, event: Button.Pressed):
        text_area = self.query_one(TextArea)
        config_text = text_area.text

        if not self._is_valid_yaml(config_text):
            self.notify(
                f"Error while saving config for: {self.model_name}; Invalid yaml format.", severity="error", timeout=5)
            return

        self.litellm_params = config_text
        new_config = yaml.safe_load(self.litellm_params)
        models = self.config.get("models", [])
        for model in models:
            if model["model_name"] == self.model_name:
                model["litellm_params"] = new_config
                break
        self.app.update_config()
        self.notify(f"Configuration saved for {self.model_name}", severity="information", timeout=3)


class ModelsList(SettingsSection):
    """Models List section component."""

    def __init__(self, **kwargs):
        super().__init__("Available Models", **kwargs)

    @property
    def config(self) -> dict:
        return self.app.config

    def compose(self) -> ComposeResult:
        yield from super().compose()

        yield ScrollableContainer(id="config-container")

    def on_mount(self) -> None:
        try:
            available_models = self.config.get("models", [])
            no_model_configured = True
            for model in available_models:
                model_name = model["model_name"]
                if model_name:
                    litellm_params = model.get("litellm_params")
                    self.add_model_config(model_name, litellm_params)
                    no_model_configured = False

            if no_model_configured:
                label = Label("No model configurations found.")
                config_container = self.query_one("#config-container")
                config_container.mount(label)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            self.notify(f"Error loading config: {str(e)}", severity="error", timeout=5)

    def add_model_config(self, model_name: str, litellm_params: dict):
        config_container = self.query_one("#config-container")
        model_config = ModelConfig(model_name, litellm_params)
        config_container.mount(model_config)
