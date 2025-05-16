from textual import on
from textual.screen import Screen
from textual.widgets import ContentSwitcher

from dasshh.ui.events import ChangeView
from dasshh.ui.views import Chat, Settings, About
from dasshh.ui.components.navbar import Navbar


class MainScreen(Screen):
    """Main screen"""

    DEFAULT_CSS = """
    MainScreen {
        layout: vertical;
        height: 1fr;
        width: 1fr;
        overflow: hidden;
    }

    ContentSwitcher {
        align: center middle;
        padding: 0 0 4 0;
    }
    """

    def compose(self):
        yield Navbar()
        with ContentSwitcher(id="content", initial="chat"):
            yield Chat(id="chat")
            yield Settings(id="settings")
            yield About(id="about")

    @on(ChangeView)
    def change_view(self, event: ChangeView):
        self.query_one(ContentSwitcher).current = event.view
