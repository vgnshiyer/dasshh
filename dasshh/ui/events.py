from typing import Dict, Any

from textual.message import Message


# -- Main screen events -- #

class ChangeView(Message):
    """Change the view on the main screen."""

    def __init__(self, view: str):
        super().__init__()
        self.view = view


# -- Chat events -- #

class NewMessage(Message):
    """Send a message to the chat."""

    def __init__(self, message: str):
        super().__init__()
        self.message = message


class LoadSession(Message):
    """Load a session."""

    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id


class DeleteSession(Message):
    """Delete an existing session."""

    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
