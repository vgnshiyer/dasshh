import json
from typing import Any

from textual.widgets import Static
from textual.reactive import reactive
from rich.syntax import Syntax
from rich.console import Group
from rich.text import Text


class Action(Static):
    """A action display component."""

    DEFAULT_CSS = """
    Action {
        width: 100%;
        margin: 1 0;
        padding: 1;
        border-left: thick $accent;
        background: $panel 15%;
    }
    """

    name: reactive[str] = reactive("", layout=True)
    args: reactive[dict] = reactive({}, layout=True)

    def __init__(self, name: str, args: dict, *a: Any, **kw: Any) -> None:
        super().__init__(*a, **kw)
        self.name = name
        self.args = args

    def render(self):
        title = Text(f"󰓦 Using tool: {self.name}", style="bold green")
        args_json = json.dumps(self.args, indent=2)
        panel_color = self.app.get_css_variables().get("panel", "")
        args_syntax = Syntax(args_json, "json", background_color=panel_color, word_wrap=True)

        return Group(
            title,
            args_syntax
        )


class ActionResult(Static):
    """A action result display component."""

    DEFAULT_CSS = """
    ActionResult {
        width: 100%;
        margin: 1 0;
        padding: 1;
        border-left: thick $success;
        background: $panel 15%;
    }
    """

    name: reactive[str] = reactive("", layout=True)
    result: reactive[dict] = reactive({}, layout=True)

    def __init__(self, name: str, result: dict, *a: Any, **kw: Any) -> None:
        super().__init__(*a, **kw)
        self.name = name
        self.result = result

    def render(self):
        title = Text(f"󰄬 Result: {self.name}", style="bold blue")
        result_json = json.dumps(self.result, indent=2)

        panel_color = self.app.get_css_variables().get("panel", "")
        result_syntax = Syntax(result_json, "json", background_color=panel_color, word_wrap=True)

        return Group(
            title,
            result_syntax
        )
