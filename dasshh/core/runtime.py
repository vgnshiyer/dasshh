import asyncio
import json
import logging
import uuid
from collections import namedtuple
from typing import Callable, AsyncGenerator

from litellm import acompletion
from litellm.types.utils import ModelResponse, ChatCompletionDeltaToolCall
from litellm.types.utils import Message

from dasshh.data.session import SessionService
from dasshh.ui.events import (
    AssistantResponseStart,
    AssistantResponseUpdate,
    AssistantResponseComplete,
    AssistantResponseError,
    AssistantToolCallStart,
    AssistantToolCallComplete,
    AssistantToolCallError,
)

logger = logging.getLogger(__name__)


InvocationContext = namedtuple(
    "InvocationContext",
    [
        "invocation_id",
        "session_id",
        "message",
        "system_instruction"
    ]
)


# remove me later
from test import get_current_weather, tools


class DasshhRuntime:
    """
    Agent runtime for Dasshh.
    """

    _model: str = "gemini/gemini-2.0-flash"
    """The model to use for the runtime."""
    _queue: asyncio.Queue
    """The queue of queries to be processed."""
    _worker: asyncio.Task
    """The worker task for the runtime."""
    _session_service: SessionService
    """The database service for the runtime."""
    _post_message_callbacks: dict[str, Callable] = {}
    """The current textual component post_message callback for sending Agent events."""
    _system_prompt: str = """
    Your name is Dasshh.
    You are a helpful assistant.
    You are able to use tools to help the user.
    Your main goal is to save user's time and effort.
    """
    """The system prompt for the runtime."""
    _default_error_response: str = "Sorry, I'm having trouble with that. Please try again later."
    """The default error response for the runtime."""
    _skip_summarization: bool = False
    """Whether to skip summarization after a tool call."""

    def __init__(self, session_service: SessionService):
        self._session_service = session_service
        self._worker = None
        self._queue = asyncio.Queue()

    @property
    def system_prompt(self) -> str:
        return {
            "role": "system",
            "content": self._system_prompt,
        }

    async def start(self):
        """Start the runtime."""
        logger.info("-- Starting Dasshh runtime --")
        self._worker = asyncio.create_task(self._process_queue())

    async def stop(self):
        """Stop the runtime."""
        if self._worker:
            logger.info("-- Stopping Dasshh runtime --")
            self._worker.cancel()
            try:
                await self._worker
            except asyncio.CancelledError:
                pass
            self._worker = None

    async def submit_query(
        self,
        *,
        message: str,
        session_id: str,
        post_message_callback: Callable,
    ) -> None:
        """
        Submit a query to the runtime.

        Args:
            message: The message to send to the runtime.
            session_id: The session id to send the message to.
            post_message_callback: The callback to post messages to the UI.
        """
        invocation_id = str(uuid.uuid4())
        logger.info(f"-- Submitting query {invocation_id} --")

        self._post_message_callbacks[invocation_id] = post_message_callback
        await self._queue.put(
            InvocationContext(
                invocation_id=invocation_id,
                message={
                    "role": "user",
                    "content": message,
                },
                session_id=session_id,
                system_instruction=False,
            )
        )

    async def _process_queue(self):
        """Process the query queue."""
        while True:
            try:
                context: InvocationContext = await self._queue.get()
                logger.info(f"-- Processing query {context.invocation_id} --")

                if not context.system_instruction:
                    self._before_query(context)
                final_response = ""
                async for response in self._run_async(context):
                    delta = response.choices[0].delta
                    if not delta.content and delta.tool_calls:
                        await self._handle_tool_calls(context, delta.tool_calls)
                        break
                    if not delta.content:
                        continue

                    final_response += delta.content
                    self._during_query(context, delta.content)

                if final_response:
                    self._after_query(context, final_response)
            except Exception as e:
                logger.error(
                    f"-- Error processing query {context.invocation_id}, {str(e)} --",
                    exc_info=True,
                )
                self._after_query(context, self._default_error_response)
                self._on_query_error(context, e)
                continue
            except asyncio.CancelledError:
                logger.info("-- query processing cancelled --")
                break

    async def _run_async(self, context: InvocationContext) -> AsyncGenerator[ModelResponse, None]:
        """Run a completion query."""
        response = await acompletion(
            model=self._model,
            messages=[self.system_prompt, context.message],
            tools=tools,
            tool_choice="auto",
            stream=True,
            n=1,
        )

        async for chunk in response:
            yield chunk

    async def _handle_tool_calls(
        self,
        context: InvocationContext,
        tool_calls: list[ChatCompletionDeltaToolCall],
    ) -> None:
        """Handle tool calls."""
        self._session_service.add_event(
            invocation_id=context.invocation_id,
            content=Message(
                role="assistant",
                tool_calls=[
                    tool_call.model_dump(exclude_unset=True, exclude_none=True)
                    for tool_call in tool_calls
                ],
            ).model_dump(exclude_unset=True, exclude_none=True),
            session_id=context.session_id,
        )
        for tool_call in tool_calls:
            tool_call_id = tool_call.id
            tool_name = tool_call.function.name
            args = tool_call.function.arguments
            self._before_tool_call(context, tool_call_id, tool_name, args)
            if tool_name == "get_current_weather":
                result = get_current_weather(**json.loads(args))
                await self._after_tool_call(context, tool_call_id, tool_name, result)

    def __get_post_message_callback(self, context: InvocationContext) -> Callable:
        """Get the post_message_callback for the query."""
        post_message_callback = self._post_message_callbacks.get(context.invocation_id, None)
        if not post_message_callback:
            logger.warning(f"-- No post_message_callback found for query {context.invocation_id} --")
            return None
        return post_message_callback

    # -- Events --

    def _before_query(self, context: InvocationContext) -> None:
        """Callback before the query is run."""
        post_message_callback = self.__get_post_message_callback(context)
        if not post_message_callback:
            return
        post_message_callback(AssistantResponseStart(invocation_id=context.invocation_id))
        self._session_service.add_event(
            invocation_id=context.invocation_id,
            content=context.message,
            session_id=context.session_id,
        )

    def _during_query(self, context: InvocationContext, content: str) -> None:
        """Callback during the query is run."""
        post_message_callback = self.__get_post_message_callback(context)
        if not post_message_callback:
            return
        post_message_callback(
            AssistantResponseUpdate(
                invocation_id=context.invocation_id,
                content=content,
            )
        )

    def _after_query(self, context: InvocationContext, content: str) -> None:
        """Callback after the query is run."""
        post_message_callback = self.__get_post_message_callback(context)
        if not post_message_callback:
            return
        post_message_callback(
            AssistantResponseComplete(
                invocation_id=context.invocation_id,
                content=content
            )
        )
        self._session_service.add_event(
            invocation_id=context.invocation_id,
            content={
                "role": "assistant",
                "content": content,
            },
            session_id=context.session_id,
        )
        self._post_message_callbacks.pop(context.invocation_id, None)

    def _on_query_error(self, context: InvocationContext, e) -> None:
        """Callback when error during query."""
        post_message_callback = self.__get_post_message_callback(context)
        if not post_message_callback:
            return
        post_message_callback(
            AssistantResponseError(
                invocation_id=context.invocation_id,
                error=str(e)
            )
        )

    def _before_tool_call(self, context: InvocationContext, tool_call_id: str, tool_name: str, args: str) -> None:
        """Callback before a tool call is run."""
        post_message_callback = self.__get_post_message_callback(context)
        if not post_message_callback:
            return
        post_message_callback(
            AssistantToolCallStart(
                invocation_id=context.invocation_id,
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                args=args,
            )
        )

    async def _after_tool_call(
        self,
        context: InvocationContext,
        tool_call_id: str,
        tool_name: str,
        result: dict,
    ) -> None:
        """Callback after a tool call is run."""
        post_message_callback = self.__get_post_message_callback(context)
        if not post_message_callback:
            return
        result_json = json.dumps(result, indent=2)
        post_message_callback(
            AssistantToolCallComplete(
                invocation_id=context.invocation_id,
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                result=result_json,
            )
        )
        self._session_service.add_event(
            invocation_id=context.invocation_id,
            content={
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": result_json,
            },
            session_id=context.session_id,
        )

        if not self._skip_summarization:
            await self._queue.put(
                InvocationContext(
                    invocation_id=context.invocation_id,
                    message={
                        "role": "user",
                        "content": f"Summarize the result of the tool call: {result_json}",
                    },
                    session_id=context.session_id,
                    system_instruction=True,
                )
            )

    def _on_tool_call_error(
        self,
        context: InvocationContext,
        tool_call_id: str,
        tool_name: str,
        error: str,
    ) -> None:
        """Callback after a tool call is run."""
        post_message_callback = self.__get_post_message_callback(context)
        if not post_message_callback:
            return
        post_message_callback(
            AssistantToolCallError(
                invocation_id=context.invocation_id,
                tool_call_id=tool_call_id,
                tool_name=tool_name,
                error=error,
            )
        )
