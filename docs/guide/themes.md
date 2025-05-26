# Themes

Dasshh supports multiple themes.

## Creating a custom theme

A theme is a simple Python object that inherits from `textual.theme.Theme`.

```python
from textual.theme import Theme

my_theme = Theme(
    name="my_theme",
    primary="#76ff03",
    secondary="#64dd17",
    accent="#4caf50",
    foreground="#f0f0f0",
    background="#101a10",
    success="#b9f6ca",
    warning="#ffff8d",
    error="#ff8a80",
    surface="#162316",
    panel="#1e2a1e",
    dark=True,
    variables={
        "footer-key-foreground": "#76ff03",
        "input-selection-background": "#64dd1740",
        "block-cursor-background": "#76ff03",
        "block-cursor-foreground": "#101a10",
        "border": "#76ff03",
        "scrollbar": "#4caf50",
        "scrollbar-hover": "#64dd17",
        "scrollbar-active": "#76ff03",
        "link-color": "#9cff57",
        "link-color-hover": "#76ff03",
    },
)
```

## Registering a theme

You can register a theme to Dasshh by overriding the `startup` method in your `App` subclass.

```python
from dasshh.ui.app import Dasshh

class MyApp(Dasshh):
    def startup(self):
        super().startup()
        self.register_theme(my_theme)
        self.theme = "my_theme"
```

Once you have registered a theme, you can toggle between themes using the `Ctrl+t` keybinding.

!!! tip
    For more information on theme variables, see the [Textual documentation](https://textual.textualize.io/guide/design/#theme-variables).

## Requesting a new theme

If you have a theme you'd like to see added to Dasshh, please [open an issue](https://github.com/vgnshiyer/dasshh/issues/new?template=theme_request.md) with your request.