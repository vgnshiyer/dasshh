# DasshhRuntime

This page lays out all the methods and attributes available on the DasshhRuntime class.

!!! tip
    DasshhRuntime is the core engine that handles AI model interactions, tool execution, and session management in Dasshh.

<!-- ----------------------- ATTRIBUTES ---------------------------------- -->

## `attr` model

The model to use for the runtime

```python
model: str = ""
```

## `attr` api_base

The base URL for the API

```python
api_base: str = ""
```

## `attr` api_key

The API key to use for the runtime

```python
api_key: str = ""
```

## `attr` api_version

The API version to use for the runtime

```python
api_version: str = ""
```

## `attr` temperature

The temperature to use for the runtime

```python
temperature: float = 1.0
```

## `attr` top_p

The top_p to use for the runtime

```python
top_p: float = 1.0
```

## `attr` max_tokens

The max_tokens to use for the runtime

```python
max_tokens: int | None = None
```

## `attr` max_completion_tokens

The max_completion_tokens to use for the runtime

```python
max_completion_tokens: int | None = None
```

## `attr` skip_summarization

Whether to skip summarization after a tool call

```python
skip_summarization: bool = False
```

<!-- ---------------- PROPERTIES ------------------------------------- -->

## `property` system_prompt

```python
system_prompt -> dict
```

Returns the system prompt as a formatted message dictionary

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| dict          |                     | System prompt formatted as a message with role and content                               |

<!-- ------------------ METHODS -------------------------------------- -->

## `method` __init__

```python
__init__(session_service: SessionService)
```

Initialize the DasshhRuntime with a session service

**Parameters:**

| Param|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| session_service |                   | The SessionService instance for managing conversations and events                         |

## `method` start

```python
async start()
```

Start the runtime worker that processes the query queue

## `method` stop

```python
async stop()
```

Stop the runtime worker and cancel any pending operations

## `method` submit_query

```python
async submit_query(
    *,
    message: str,
    session_id: str,
    post_message_callback: Callable,
) -> None
```

Submit a query to the runtime for processing

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| message | | The user message to send to the AI |
| session_id | | The session ID to associate with this conversation |
| post_message_callback | | Callback function to send UI events back to the interface |

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| None          |                     | This method is async and doesn't return a value                                          |

<!-- ------------------ PRIVATE METHODS -------------------------------------- -->

## `method` _load_model_config

```python
_load_model_config() -> None
```

Load model configuration from the config file

**Raises:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| ValueError    |                     | If API key is not set in configuration                                                   |

## `method` _generate_prompt

```python
_generate_prompt(context: InvocationContext) -> List[dict]
```

Generate the complete prompt including system message and conversation history

**Parameters:**

| Param|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| context       |                     | The invocation context containing session and message information                         |

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| List[dict]    |                     | List of message dictionaries formatted for the AI model                                  |

## `method` _process_queue

```python
async _process_queue()
```

Main worker loop that processes queries from the queue

## `method` _run_async

```python
async _run_async(context: InvocationContext) -> AsyncGenerator[ModelResponse, None]
```

Execute the AI completion request and yield streaming responses

**Parameters:**

| Param|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| context       |                     | The invocation context for this query                                                    |

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| AsyncGenerator |                    | Stream of model responses                                                                 |

## `method` _handle_tool_calls

```python
async _handle_tool_calls(
    context: InvocationContext,
    tool_calls: list[ChatCompletionDeltaToolCall],
) -> None
```

Process and execute tool calls from the AI model

**Parameters:**

| Param|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| context       |                     | The invocation context                                                                    |
| tool_calls    |                     | List of tool calls to execute                                                             |

## InvocationContext:

A named tuple to store current query context.

| Param | Type | Description |
|-------|------|-------------|
| invocation_id | str | The ID of the invocation |
| message | dict | The message to send to the LLM |
| session_id | str | The ID of the session |
| system_instruction | bool | Whether to use the system instruction |
