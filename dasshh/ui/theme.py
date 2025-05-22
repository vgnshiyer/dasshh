from textual.theme import Theme

lime_theme = Theme(
    name="lime",
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
