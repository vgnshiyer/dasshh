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


class NewSession(Message):
    """Create a new session."""

    def __init__(self):
        super().__init__()


class LoadSession(Message):
    """Load a previous session."""

    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id


class DeleteSession(Message):
    """Delete an existing session."""

    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id


# -- Agent runtime events -- #


class AssistantResponseStart(Message):
    """Event triggered before agent starts processing a query."""

    def __init__(self, invocation_id: str):
        super().__init__()
        self.invocation_id = invocation_id


class AssistantResponseUpdate(Message):
    """Event triggered when agent returns a partial response."""

    def __init__(self, invocation_id: str, content: str):
        super().__init__()
        self.invocation_id = invocation_id
        self.content = content


class AssistantResponseComplete(Message):
    """Event triggered when agent completes processing a query."""

    def __init__(self, invocation_id: str, content: str):
        super().__init__()
        self.invocation_id = invocation_id
        self.content = content


class AssistantResponseError(Message):
    """Event triggered when agent encounters an error."""

    def __init__(self, invocation_id: str, error: str):
        super().__init__()
        self.invocation_id = invocation_id
        self.error = error


class AssistantToolCallStart(Message):
    """Event triggered when agent starts a tool call."""

    def __init__(
        self, invocation_id: str, tool_call_id: str, tool_name: str, args: str
    ):
        super().__init__()
        self.invocation_id = invocation_id
        self.tool_call_id = tool_call_id
        self.tool_name = tool_name
        self.args = args


class AssistantToolCallComplete(Message):
    """Event triggered when agent completes a tool call."""

    def __init__(
        self, invocation_id: str, tool_call_id: str, tool_name: str, result: str
    ):
        super().__init__()
        self.invocation_id = invocation_id
        self.tool_call_id = tool_call_id
        self.tool_name = tool_name
        self.result = result


class AssistantToolCallError(Message):
    """Event triggered when agent encounters an error during a tool call."""

    def __init__(
        self, invocation_id: str, tool_call_id: str, tool_name: str, error: str
    ):
        super().__init__()
        self.invocation_id = invocation_id
        self.tool_call_id = tool_call_id
        self.tool_name = tool_name
        self.error = error
