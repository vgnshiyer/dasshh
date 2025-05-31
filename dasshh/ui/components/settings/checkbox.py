from textual.widgets._checkbox import Checkbox as TextualCheckbox
from textual.content import Content


class Checkbox(TextualCheckbox):
    """A checkbox widget that displays a checkmark or cross."""

    DEFAULT_CSS = """
    Checkbox {
        & > .toggle--button {
            color: $secondary;
            background: $background;
        }

        &.-on > .toggle--button {
            color: $primary;
            background: $background;
        }
    }
    """

    checked_label = "✓"
    unchecked_label = "✗"

    def render(self) -> Content:
        """Render the content of the widget."""
        button_style = self.get_visual_style("toggle--button")
        label_style = self.get_visual_style("toggle--label")
        label = self._label.stylize_before(label_style)
        spacer = " " if label else ""

        if self.value:
            button = (self.checked_label, button_style)
        else:
            button = (self.unchecked_label, button_style)

        if self._button_first:
            content = Content.assemble(button, spacer, label)
        else:
            content = Content.assemble(label, spacer, button)
        return content
