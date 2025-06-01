from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label


class SettingsSection(Container):
    """A section container for grouping related settings."""

    DEFAULT_CSS = """
    SettingsSection {
        layout: vertical;
        width: 100%;
        height: auto;
        padding: 2;
        border: round $secondary;
    }

    SettingsSection > .section-title {
        text-style: bold;
        color: $primary;
        margin-top: 0;
        margin-bottom: 1;
        dock: top;
    }

    SettingsSection > Static {
        margin-top: 1;
        margin-left: 1;
    }

    SettingsSection > Input,
    SettingsSection > Checkbox,
    SettingsSection > Select {
        border: round $secondary;
        background: $background;

        &:focus, &:hover {
            border: round $primary;
            background: $background;
            background-tint: $background;
        }

        &:disabled {
            border: round $panel-darken-1;
            color: $text-muted;
        }

        &.-invalid, &.-invalid:focus {
            border: round $error;
            background: $background;
            background-tint: $background;
        }
    }

    SettingsSection > Input {
        width: 75%;
    }

    SettingsSection > Checkbox {
        width: 25%;
        margin-left: 0;
        margin-top: 1;
    }

    SettingsSection > Select {
        width: 75%;

        & > SelectCurrent, &:focus > SelectCurrent {
            border: none;
            background: $background;
            background-tint: $background;
        }

        & > SelectOverlay {
            border: round $primary;
            background: $background;
            background-tint: $background;
            scrollbar-color: $secondary $background;
            scrollbar-background: $background;
            scrollbar-corner-color: $background;
            scrollbar-size: 1 1;
            scrollbar-gutter: stable;
        }
    }
    """

    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title, classes="section-title")
