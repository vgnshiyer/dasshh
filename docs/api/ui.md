# UI

This page lays out all the classes and utilities available in the Dasshh UI module.

## UI Architecture

### Component Hierarchy

```
Dasshh (App)
└── MainScreen
    ├── Navbar
    └── ContentSwitcher
        ├── Chat (View)
        │   ├── HistoryPanel
        │   ├── ChatPanel
        │   └── ActionsPanel
        ├── Settings (View)
        └── About (View)
```

### Component Categories

1. **Screens** - Top-level containers (MainScreen, HelpScreen)
2. **Views** - Content areas within screens (Chat, Settings, About)
3. **Components** - Reusable UI elements (Navbar, ChatPanel, etc.)

### Data Flow

1. **User Input** → UI Components → Events
2. **Events** → Runtime → AI Processing
3. **AI Responses** → Events → UI Updates
4. **Database** ↔ SessionService ↔ UI Components

### Event-Driven Architecture

- UI components communicate via Textual's Message system
- Events defined in `dasshh.ui.events` module
- Runtime publishes events back to UI via callbacks
- State management through session persistence


## Main Application

### `class` Dasshh

Main application class that extends Textual's App

```python
class Dasshh(App)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| SCREENS | dict | Available screens mapped by name |
| BINDINGS | list | Key bindings for the application |
| logger | logging.Logger | Application logger instance |
| runtime | DasshhRuntime | AI runtime engine for processing queries |
| session_service | SessionService | Database service for managing sessions |

### `method` __init__

```python
__init__(*args, **kwargs)
```

Initialize the Dasshh application

**Behavior:**

- Loads configuration file
- Loads and registers tools
- Initializes database and runtime services
- Sets up logging

### `method` on_mount

```python
async on_mount()
```

Application mount lifecycle method

### `method` on_unmount

```python
async on_unmount()
```

Application unmount lifecycle method

## UI Types

Type definitions for UI components using Pydantic models.

### `type` UIMessage

Message model for displaying chat messages in the UI

```python
class UIMessage(BaseModel)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | The invocation ID of the message (optional, defaults to "") |
| role | Literal["user", "assistant"] | The role of the message sender |
| content | str | The text content of the message |

**Usage:**
```python
message = UIMessage(
    invocation_id="inv_123",
    role="user", 
    content="Hello, how are you?"
)
```

### `type` UIAction

Action model for displaying tool calls and results in the UI

```python
class UIAction(BaseModel)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| tool_call_id | str | Unique identifier for the tool call |
| invocation_id | str | The invocation ID this action belongs to |
| name | str | Name of the tool that was called |
| args | str | JSON string of arguments passed to the tool (formatted with indent=2) |
| result | str | JSON string of the tool's return value (formatted with indent=2) |

**Usage:**
```python
action = UIAction(
    tool_call_id="call_123",
    invocation_id="inv_456",
    name="get_weather",
    args='{\n  "city": "San Francisco"\n}',
    result='{\n  "temperature": 72,\n  "condition": "sunny"\n}'
)
```

### `type` UISession

Session model for displaying chat sessions in the UI

```python
class UISession(BaseModel)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| id | str | Unique identifier for the session |
| detail | str | Brief description or preview of the session |
| created_at | datetime | When the session was created |
| updated_at | datetime | When the session was last updated |
| messages | List[UIMessage] | All messages in the session |
| actions | List[UIAction] | All tool actions in the session |

## Usage Patterns

### Basic Application Setup

```python
from dasshh.ui.app import Dasshh

# Create and run application
app = Dasshh()
app.run()
```

### Working with UI Types

```python
from dasshh.ui.types import UIMessage, UIAction, UISession
from dasshh.ui.utils import convert_session_obj

# Convert database session to UI session
ui_session = convert_session_obj(db_session, events)

# Access messages and actions
for message in ui_session.messages:
    print(f"{message.role}: {message.content}")

for action in ui_session.actions:
    print(f"Tool: {action.name}, Result: {action.result}")
```

### Configuration Management

```python
from dasshh.ui.utils import load_config, get_from_config

# Initialize config
load_config()

# Read configuration values
model_name = get_from_config("model.name")
api_key = get_from_config("model.api_key")
```

## Chat Components

The main UI components that make up the three-panel chat interface.

### `class` ChatPanel

Main chat panel containing the chat history and input area

```python
class ChatPanel(Widget)
```

**Methods:**

| Method | Parameters | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| `reset()` | None | Clears all messages and shows a default message. Disables chat input |
| `load_messages()` | messages: List[UIMessage] | Loads messages from a previous chat session and enables input |
| `add_new_message()` | message: UIMessage | Adds a new message to the chat history and scrolls to bottom |
| `update_assistant_message()` | invocation_id: str, content: str, final: bool | Updates streaming assistant messages |
| `get_message_widget()` | invocation_id: str | Returns the ChatMessage widget for given invocation ID |

**Usage:**
```python
# Reset panel
chat_panel.reset()

# Load previous messages
chat_panel.load_messages(ui_session.messages)

# Add new message
new_message = UIMessage(role="user", content="Hello!")
chat_panel.add_new_message(new_message)

# Update streaming response
chat_panel.update_assistant_message(
    invocation_id="inv_123",
    content="Hello! How can I help?",
    final=True
)
```

### `class` HistoryPanel

Sessions panel for managing chat history and creating new sessions

```python
class HistoryPanel(Widget)
```

**Methods:**

| Method | Parameters | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| `load_sessions()` | sessions: List[UISession], current: str | Loads all sessions and marks current one |
| `add_session()` | session: UISession | Adds a new session to the panel |
| `set_current_session()` | session_id: str | Updates visual selection of current session |
| `get_history_item_widget()` | session_id: str | Returns HistoryItem widget for given session |

**Events Generated:**

- `NewSession` - When "New Session" button is pressed
- `LoadSession` - When a session is clicked
- `DeleteSession` - When delete icon is clicked

**Usage:**
```python
# Load sessions with current selection
history_panel.load_sessions(all_sessions, current_session_id)

# Add new session
new_session = UISession(id="sess_123", detail="New conversation")
history_panel.add_session(new_session)

# Update current selection
history_panel.set_current_session("sess_456")
```

### `class` ActionsPanel

Actions panel for displaying tool calls and their results

```python
class ActionsPanel(Widget)
```

**Methods:**

| Method | Parameters | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| `reset()` | None | Clears all actions from the panel |
| `load_actions()` | actions: List[UIAction] | Loads actions from a previous session |
| `add_action()` | action: UIAction | Adds a new tool action to the panel |
| `update_action()` | invocation_id: str, tool_call_id: str, result: str | Updates action with result |
| `get_action_widget()` | invocation_id: str, tool_call_id: str | Returns Action widget for given IDs |
| `handle_error()` | error: str | Shows error notification for failed tools |

**Usage:**
```python
# Reset panel
actions_panel.reset()

# Load previous actions
actions_panel.load_actions(ui_session.actions)

# Add new action
new_action = UIAction(
    tool_call_id="call_123",
    invocation_id="inv_456", 
    name="get_weather",
    args='{"city": "San Francisco"}',
    result=""
)
actions_panel.add_action(new_action)

# Update with result
actions_panel.update_action(
    invocation_id="inv_456",
    tool_call_id="call_123",
    result='{"temperature": 72}'
)
```

## Component Sub-Elements

Individual components used within the main panels.

### `class` ChatMessage

Individual message display component

```python
class ChatMessage(Static)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Links message to specific invocation |
| role | str | Either "you" or "dasshh" (converted from "user"/"assistant") |
| content | str | Message text content (reactive, triggers re-render) |
| user_icon | str | Icon for user messages |
| assistant_icon | str | Icon for assistant messages |

### `class` Action

Individual tool action display component

```python
class Action(Static)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | str | Links action to specific invocation |
| tool_call_id | str | Unique identifier for this tool call |
| name | str | Name of the tool being called |
| args | str | JSON-formatted tool arguments |
| result | str | JSON-formatted tool result |

### `class` HistoryItem

Individual session item in history panel

```python
class HistoryItem(Static)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | str | Unique session identifier |
| detail | str | Session preview text (truncated to 40 chars) |
| created_at | datetime | Session creation timestamp |
| selected | bool | Whether this session is currently active |

**Events Generated:**
- `LoadSession` - When clicked

### `class` DeleteIcon

Delete button for session items

```python
class DeleteIcon(Static)
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | str | Session to delete when clicked |
| selected | bool | Matches parent HistoryItem selection state |

**Events Generated:**
- `DeleteSession` - When clicked

## Event Handling

### Component Communication

Components communicate via Textual's message system:

```python
# Session management
self.post_message(NewSession())
self.post_message(LoadSession(session_id))
self.post_message(DeleteSession(session_id))

# Handle events
@on(LoadSession)
def handle_load_session(self, event: LoadSession):
    # Load session by ID
    pass
```

### State Management

Components maintain state through reactive attributes:

```python
# Reactive updates trigger re-renders
message.content = "New content"  # Auto-updates display
action.result = json.dumps(result)  # Updates result display
history_item.selected = True  # Updates visual selection
```

### Error Handling

```python
# Actions panel handles tool errors
actions_panel.handle_error("Tool execution failed")

# Shows toast notification to user
# Uses Textual's notification system
```
