from typing import List
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.app import ComposeResult
from textual import on
from litellm.types.utils import Message, ChatCompletionMessageToolCall, Function

from dasshh.data.session import SessionService, Session
from dasshh.core.logging import get_logger
from dasshh.core.runtime import DasshhRuntime
from dasshh.ui.components.chat import ChatPanel, HistoryPanel, ActionsPanel
from dasshh.ui.components.chat.chat_input import ChatInput
from dasshh.ui.events import (
    NewMessage,
    AssistantResponseStart,
    AssistantResponseUpdate,
    AssistantResponseComplete,
    AssistantResponseError,
    AssistantToolCallStart,
    AssistantToolCallComplete,
    AssistantToolCallError,
    LoadSession,
    NewSession,
    DeleteSession
)

logger = get_logger("dasshh.views.chat")


class Chat(Widget):

    DEFAULT_CSS = """
    Chat {
        layout: vertical;
        height: 1fr;
        width: 1fr;
        align: center middle;
    }

    #chat-history { width: 20%; }
    #chat-panel { width: 45%; }
    #chat-actions { width: 35%; }
    """

    current_session_id: str = ""
    """The current session id."""

    DEFAULT_GREETING = "Hi! How can I help you today?"

    @property
    def session_service(self) -> SessionService:
        """Get the session service."""
        return self.app.session_service

    @property
    def runtime(self) -> DasshhRuntime:
        """Get the app's assistant runtime."""
        return self.app.runtime

    @property
    def chat_panel(self):
        """Get the chat panel widget."""
        return self.query_one(ChatPanel)

    @property
    def actions_panel(self):
        """Get the actions panel widget."""
        return self.query_one(ActionsPanel)

    @property
    def history_panel(self):
        """Get the history panel widget."""
        return self.query_one(HistoryPanel)

    def compose(self) -> ComposeResult:
        logger.debug("Composing Chat view")
        with Horizontal(id="chat-container"):
            with Vertical(id="chat-history"):
                yield HistoryPanel()
            with Vertical(id="chat-panel"):
                yield ChatPanel()
            with Vertical(id="chat-actions"):
                yield ActionsPanel()

    def on_mount(self) -> None:
        """Chat view mounted."""
        self.chat_panel.query_one(ChatInput).disable()
        self._load_data()

    def _load_data(self) -> None:
        """Load previous sessions and chats."""
        # load recent session
        recent_session: Session = (
            self.session_service.get_recent_session()
            or self.session_service.new_session()
        )
        self.current_session_id = recent_session.id

        # load history panel
        all_sessions: List[Session] = self.session_service.list_sessions()
        self.history_panel.load_sessions(all_sessions, current=self.current_session_id)

        # load chat panel and actions panel
        messages, actions = [], []
        for event in recent_session.events:
            if event.tool_calls:
                actions.extend(event.tool_calls)
            elif event.role == "tool":
                actions.append(event)
            else:
                messages.append(event)

        self.chat_panel.load_messages(messages)
        self.actions_panel.load_actions(actions)

    # -- Handlers --

    @on(LoadSession)
    def on_load_session(self, event: LoadSession) -> None:
        """Handle when a previous session is loaded."""
        self.current_session_id = event.session_id
        self.history_panel.set_current_session(self.current_session_id)

    @on(NewSession)
    def on_new_session(self, _: NewSession) -> None:
        """Handle when a new session is created."""
        self.current_session_id = self.session_service.new_session().id
        self.history_panel.set_current_session(self.current_session_id)

    @on(DeleteSession)
    def on_delete_session(self, event: DeleteSession) -> None:
        """Handle when a session is deleted."""
        logger.debug(f"Deleting session {event.session_id}")
        if event.session_id == self.current_session_id:
            self.chat_panel.reset()
            self.actions_panel.reset()
        self.session_service.delete_session(session_id=event.session_id)

    @on(NewMessage)
    async def on_new_message(self, event: NewMessage) -> None:
        """Handle when a message is sent.

        This is captured at the Chat level and forwards to runtime with this component's
        post_message, so all child components can receive assistant events.
        """
        self.chat_panel.add_new_message(Message(role="user", content=event.message))
        current_session_widget = self.history_panel.get_history_item_widget(self.current_session_id)
        if current_session_widget:
            current_session_widget.detail = event.message
            self.session_service.update_session(
                session_id=self.current_session_id,
                detail=event.message
            )

        logger.debug(f"Submitting query {event.message} to runtime")
        await self.runtime.submit_query(
            message=event.message,
            session_id=self.current_session_id,
            post_message_callback=self.post_message
        )

    @on(AssistantResponseStart)
    def on_assistant_response_start(self, _: AssistantResponseStart) -> None:
        """Handle when the assistant starts processing a response."""
        self.chat_panel.add_new_message(Message(role="assistant", content=""))

    @on(AssistantResponseUpdate)
    def on_assistant_response_update(self, event: AssistantResponseUpdate) -> None:
        """Handle when the assistant updates the response."""
        self.chat_panel.update_assistant_message(content=event.content, final=False)

    @on(AssistantResponseComplete)
    def on_assistant_response_complete(self, event: AssistantResponseComplete) -> None:
        """Handle when the assistant completes processing a response."""
        self.chat_panel.update_assistant_message(content=event.content, final=True)

    @on(AssistantResponseError)
    def on_assistant_response_error(self, event: AssistantResponseError) -> None:
        """Handle when the assistant encounters an error."""
        self.chat_panel.handle_error(event.error)

    @on(AssistantToolCallStart)
    def on_assistant_tool_call_start(self, event: AssistantToolCallStart) -> None:
        """Handle when the assistant starts a tool call."""
        self.actions_panel.add_action(
            ChatCompletionMessageToolCall(function=Function(name=event.tool_name, arguments=event.args))
        )

    @on(AssistantToolCallComplete)
    def on_assistant_tool_call_complete(self, event: AssistantToolCallComplete) -> None:
        """Handle when the assistant completes a tool call."""
        self.actions_panel.add_action(
            Message(role="tool", content=event.result, name=event.tool_name)
        )

    @on(AssistantToolCallError)
    def on_assistant_tool_call_error(self, event: AssistantToolCallError) -> None:
        """Handle when the assistant encounters an error during a tool call."""
        logger.error(
            f"Tool call error: {event.error} \n"
            f"invocation_id: {event.invocation_id}, tool_name: {event.tool_name}"
        )
        self.actions_panel.handle_error(event.error)
