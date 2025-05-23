# Events

Dasshh uses an [event-queue messaging architecture](https://blog.vgnshiyer.dev/posts/04-27-2025_event_queue_messaging_archetype) to update the UI with events.

This page lays out all the event classes available.

!!! note
    Events in Dasshh are based on Textual's [Message system](https://textual.textualize.io/guide/events/)

<!-- ----------------------- UI EVENTS ---------------------------------- -->

## UI Events

Events related to user interface interactions and navigation.

### `event` ChangeView

Change the view on the main screen

```python
class ChangeView(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| view | str | The name of the view to switch to |

**Constructor:**

```python
ChangeView(view: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| view | | The target view name (e.g., "chat", "settings", "about") |

<!-- ----------------------- CHAT EVENTS ---------------------------------- -->

## Chat Events

Events related to chat interactions and session management.

### `event` NewMessage

Send a message to the chat

```python
class NewMessage(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| message | str | The message content to send |

**Constructor:**

```python
NewMessage(message: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| message | | The user message to send to the assistant |

### `event` NewSession

Create a new session

```python
class NewSession(Message)
```

**Constructor:**

```python
NewSession()
```

**Notes:**
- This event triggers the creation of a new chat session
- No parameters required

### `event` LoadSession

Load a previous session

```python
class LoadSession(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | str | The ID of the session to load |

**Constructor:**

```python
LoadSession(session_id: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | | The unique identifier of the session to load |

### `event` DeleteSession

Delete an existing session

```python
class DeleteSession(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | str | The ID of the session to delete |

**Constructor:**

```python
DeleteSession(session_id: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | | The unique identifier of the session to delete |

<!-- ----------------------- ASSISTANT EVENTS ---------------------------------- -->

## Assistant Runtime Events

Events related to AI assistant processing and responses.

### `event` AssistantResponseStart

Event triggered before assistant starts processing a query

```python
class AssistantResponseStart(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Unique identifier for this query invocation |

**Constructor:**

```python
AssistantResponseStart(invocation_id: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Unique ID to track this specific query through its lifecycle |

### `event` AssistantResponseUpdate

Event triggered when assistant returns a partial response (streaming)

```python
class AssistantResponseUpdate(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Unique identifier for this query invocation |
| content | str | Partial content of the response |

**Constructor:**

```python
AssistantResponseUpdate(invocation_id: str, content: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Unique ID to track this specific query |
| content | | The partial response content to append |

### `event` AssistantResponseComplete

Event triggered when assistant completes processing a query

```python
class AssistantResponseComplete(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Unique identifier for this query invocation |
| content | str | Final complete content of the response |

**Constructor:**

```python
AssistantResponseComplete(invocation_id: str, content: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Unique ID to track this specific query |
| content | | The final complete response content |

### `event` AssistantResponseError

Event triggered when assistant encounters an error

```python
class AssistantResponseError(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Unique identifier for this query invocation |
| error | str | Error message describing what went wrong |

**Constructor:**

```python
AssistantResponseError(invocation_id: str, error: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Unique ID to track this specific query |
| error | | Description of the error that occurred |

<!-- ----------------------- TOOL CALL EVENTS ---------------------------------- -->

## Tool Call Events

Events related to tool execution during assistant processing.

### `event` AssistantToolCallStart

Event triggered when assistant starts a tool call

```python
class AssistantToolCallStart(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Unique identifier for the query invocation |
| tool_call_id | str | Unique identifier for this specific tool call |
| tool_name | str | Name of the tool being called |
| args | str | JSON string of arguments passed to the tool |

**Constructor:**

```python
AssistantToolCallStart(invocation_id: str, tool_call_id: str, tool_name: str, args: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Unique ID to track the query |
| tool_call_id | | Unique ID for this tool call within the query |
| tool_name | | Name of the tool being executed |
| args | | JSON-encoded arguments being passed to the tool |

### `event` AssistantToolCallComplete

Event triggered when assistant completes a tool call

```python
class AssistantToolCallComplete(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Unique identifier for the query invocation |
| tool_call_id | str | Unique identifier for this specific tool call |
| tool_name | str | Name of the tool that was called |
| result | str | JSON string of the tool's return value |

**Constructor:**

```python
AssistantToolCallComplete(invocation_id: str, tool_call_id: str, tool_name: str, result: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Unique ID to track the query |
| tool_call_id | | Unique ID for this tool call within the query |
| tool_name | | Name of the tool that was executed |
| result | | JSON-encoded result returned by the tool |

### `event` AssistantToolCallError

Event triggered when assistant encounters an error during a tool call

```python
class AssistantToolCallError(Message)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Unique identifier for the query invocation |
| tool_call_id | str | Unique identifier for this specific tool call |
| tool_name | str | Name of the tool that failed |
| error | str | Error message describing what went wrong |

**Constructor:**

```python
AssistantToolCallError(invocation_id: str, tool_call_id: str, tool_name: str, error: str)
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Unique ID to track the query |
| tool_call_id | | Unique ID for this tool call within the query |
| tool_name | | Name of the tool that encountered an error |
| error | | Description of the error that occurred |

<!-- ----------------------- EVENT FLOW ---------------------------------- -->

## Event Flow

Understanding how events flow through the system:

### Query Processing Flow

1. **User Input**: `NewMessage` → User types a message
2. **Assistant Start**: `AssistantResponseStart` → Processing begins
3. **Streaming Updates**: `AssistantResponseUpdate` → Partial responses (optional)
4. **Tool Execution** (if needed):
    - `AssistantToolCallStart` → Tool begins execution
    - `AssistantToolCallComplete` → Tool finishes successfully
    - `AssistantToolCallError` → Tool encounters error (alternative)
5. **Assistant Complete**: `AssistantResponseComplete` → Final response
6. **Error Handling**: `AssistantResponseError` → If processing fails (alternative)

### Session Management Flow

1. **Create**: `NewSession` → Creates a new conversation
2. **Load**: `LoadSession` → Switches to existing conversation  
3. **Delete**: `DeleteSession` → Removes conversation from history

### UI Navigation Flow

- **View Change**: `ChangeView` → Switches between app sections (chat, settings, about)
