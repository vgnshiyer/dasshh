# DasshhRuntime

This page lays out all the methods and attributes available on the DasshhRuntime class.

!!! tip
    DasshhRuntime is the core engine that handles AI model interactions, tool execution, and session management in Dasshh.

<!-- ----------------------- ATTRIBUTES ---------------------------------- -->

## `attr` model_config

The model configuration dictionary containing all LiteLLM parameters

```python
model_config: dict = {}
```

This dictionary contains the complete model configuration (via `litellm_params` key) including:

- `model`: The model provider and name (e.g., "gemini/gemini-2.0-flash")
- `api_key`: The API key for the chosen provider
- `api_base`: The base URL for the API (optional)
- `api_version`: The API version to use (optional)
- `temperature`: The temperature for the model (default: 1.0)
- `top_p`: The top_p value for the model (default: 1.0)
- `max_tokens`: The maximum number of tokens to generate
- `max_completion_tokens`: The maximum number of tokens for completion

## `attr` system_prompt

The system prompt for the runtime

```python
system_prompt: str = "Your name is Dasshh..."
```

## `attr` skip_summarization

Whether to skip summarization after a tool call

```python
skip_summarization: bool = False
```

<!-- ---------------- PROPERTIES ------------------------------------- -->

## `property` get_system_prompt

```python
get_system_prompt() -> dict
```

Returns the system prompt as a formatted message dictionary

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| dict          |                     | System prompt formatted as a message with role and content                               |

<!-- ------------------ METHODS -------------------------------------- -->

## `method` __init__

```python
__init__(
    *,
    session_service: SessionService,
    model_config: dict = {},
    system_prompt: str = "",
    skip_summarization: bool = False,
)
```

Initialize the DasshhRuntime with configuration parameters

**Parameters:**

| Param|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| session_service |                   | The SessionService instance for managing conversations and events                         |
| model_config | {} | Dictionary containing LiteLLM model configuration parameters |
| system_prompt | "" | Custom system prompt for the assistant |
| skip_summarization | False | Whether to skip summarization after tool calls |

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

Handle tool calls from the AI model

**Parameters:**

| Param|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| context       |                     | The invocation context for this query                                                    |
| tool_calls    |                     | List of tool calls from the AI model                                                     |

## Configuration Integration

The DasshhRuntime receives its model configuration from the Dasshh app, which manages multiple model configurations:

```python
# Example of how the runtime is configured
runtime = DasshhRuntime(
    session_service=session_service,
    model_config={
        "model_name": "gemini-flash",
        "litellm_params": {
            "model": "gemini/gemini-2.0-flash",
            "api_key": "your-api-key",
            "temperature": 0.7,
            "max_tokens": 2000
        }
    },
    system_prompt="Your custom system prompt",
    skip_summarization=False
)
```

The model configuration corresponds to the `litellm_params` section of a model entry in the configuration file.
