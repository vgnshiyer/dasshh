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
        border-left: thick $success;
        background: $panel 15%;
    }
    """

    name: reactive[str] = reactive("", layout=True)
    args: reactive[str] = reactive("", layout=True)
    result: reactive[str] = reactive("", layout=True)

    def __init__(
        self,
        invocation_id: str,
        tool_call_id: str,
        name: str,
        args: str,
        result: str,
        *a: Any,
        **kw: Any,
    ) -> None:
        super().__init__(*a, **kw)
        self.invocation_id = invocation_id
        self.tool_call_id = tool_call_id
        self.name = name
        self.args = args
        self.result = result

    def render(self):
        tool_call_title = Text(f"󰓦 Using tool: {self.name}", style="bold green")
        panel_color = self.app.get_css_variables().get("panel", "")
        args_syntax = Syntax(
            self.args, "json", background_color=panel_color, word_wrap=True
        )

        if self.result:
            result_title = Text(f"󰄬 Result: {self.name}", style="bold blue")
            result_syntax = Syntax(
                self.result, "json", background_color=panel_color, word_wrap=True
            )
            return Group(
                tool_call_title, args_syntax, Text(""), result_title, result_syntax
            )
        else:
            return Group(tool_call_title, args_syntax)
