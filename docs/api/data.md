# Data

This page lays out all the classes and methods available in the Dasshh data module.

!!! tip
    The data module handles persistence using SQLite and SQLAlchemy for managing chat sessions, conversation history, and tool execution events.

<!-- ----------------------- MODELS ---------------------------------- -->

## Database Models

SQLAlchemy models that define the database schema.

### `model` StorageSession

Database model for storing chat sessions

```python
class StorageSession(Base)
```

**Table:** `sessions`

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| id | str | Primary key, UUID string automatically generated |
| detail | str | Brief description or preview of the session content |
| created_at | datetime | Timestamp when the session was created (UTC) |
| updated_at | datetime | Timestamp when the session was last updated (UTC) |
| events | relationship | Related StorageEvent objects for this session |

**Database Schema:**

```sql
CREATE TABLE sessions (
    id VARCHAR PRIMARY KEY,
    detail VARCHAR,
    created_at DATETIME,
    updated_at DATETIME
);
```

### `model` StorageEvent

Database model for storing conversation events and tool executions

```python
class StorageEvent(Base)
```

**Table:** `events`

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| id | str | Primary key, UUID string automatically generated |
| invocation_id | str | Identifier linking events to a specific query invocation |
| session_id | str | Foreign key referencing sessions.id |
| created_at | datetime | Timestamp when the event was created (UTC) |
| content | JSON | Event data stored as JSON (messages, tool calls, etc.) |
| session | relationship | Related StorageSession object |

**Database Schema:**

```sql
CREATE TABLE events (
    id VARCHAR PRIMARY KEY,
    invocation_id VARCHAR,
    session_id VARCHAR REFERENCES sessions(id),
    created_at DATETIME,
    content JSON
);
```

<!-- ----------------------- CLIENT ---------------------------------- -->

## Database Client

### `class` Base

SQLAlchemy declarative base class for all database models

```python
class Base(DeclarativeBase)
```

**Usage:**
- Parent class for all database models
- Provides SQLAlchemy ORM functionality

### `class` DBClient

Database client for managing SQLite connections

```python
class DBClient
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| db_path | Path | Path to SQLite database file (~/.dasshh/db/dasshh.db) |
| engine | Engine | SQLAlchemy database engine |
| DatabaseSessionFactory | sessionmaker | Session factory for creating database sessions |

### `method` __init__

```python
__init__()
```

Initialize the database client and create necessary directories and tables

**Behavior:**
- Creates ~/.dasshh/db/ directory if it doesn't exist
- Creates SQLite database file
- Sets up SQLAlchemy engine and session factory
- Creates all database tables defined in models

### `method` get_db

```python
get_db() -> Generator[Session, None, None]
```

Get a database session for executing queries

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| Generator[Session, None, None] | | SQLAlchemy database session |

**Usage:**
```python
with db_client.get_db() as db:
    # Use db session here
    result = db.query(StorageSession).all()
```

<!-- ----------------------- SESSION SERVICE ---------------------------------- -->

## Session Service

### `class` SessionService

Service class for managing chat sessions and events

```python
class SessionService
```

**Attributes:**

| Attribute | Type | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| db_client | DBClient | Database client instance for database operations |

### `method` __init__

```python
__init__(db_client: DBClient)
```

Initialize the session service with a database client

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| db_client | | DBClient instance for database operations |

### `method` new_session

```python
new_session(detail: str = "New Session") -> StorageSession
```

Create a new chat session

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| detail | "New Session" | Brief description or preview text for the session |

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| StorageSession | | The newly created session object |

### `method` get_session

```python
get_session(*, session_id: str) -> StorageSession | None
```

Retrieve a specific session by its ID

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | | Unique identifier of the session to retrieve |

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| StorageSession \| None | | The session object, or None if not found |

### `method` get_events

```python
get_events(*, session_id: str) -> list[StorageEvent]
```

Get all events for a specific session

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | | Unique identifier of the session |

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| list[StorageEvent] | | List of all events in the session |

### `method` get_recent_session

```python
get_recent_session() -> StorageSession | None
```

Get the most recently updated session

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| StorageSession \| None | | The most recent session, or None if no sessions exist |

### `method` update_session

```python
update_session(*, session_id: str, detail: str) -> None
```

Update a session's detail and timestamp

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | | Unique identifier of the session to update |
| detail | | New detail text for the session |

### `method` list_sessions

```python
list_sessions(include_events: bool = False) -> list[StorageSession]
```

List all sessions in the database

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| include_events | False | Whether to load related events for each session |

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| list[StorageSession] | | List of all sessions |

**Notes:**
- When `include_events=False`, related events are not loaded for better performance
- When `include_events=True`, all related events are loaded via SQLAlchemy relationships

### `method` delete_session

```python
delete_session(*, session_id: str) -> None
```

Delete a session and all its related events

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| session_id | | Unique identifier of the session to delete |

**Notes:**
- Cascading delete removes all related events automatically
- No error if session doesn't exist

### `method` add_event

```python
add_event(*, invocation_id: str, session_id: str, content: dict) -> None
```

Add a new event to a session

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| invocation_id | | Identifier linking this event to a query invocation |
| session_id | | Unique identifier of the session |
| content | | Event data as a dictionary (will be stored as JSON) |

**Event Content Examples:**

```python
# User message
content = {
    "role": "user",
    "content": "Hello, how are you?"
}

# Assistant response
content = {
    "role": "assistant", 
    "content": "I'm doing well, thank you!"
}

# Tool call
content = {
    "role": "assistant",
    "tool_calls": [
        {
            "id": "call_123",
            "function": {
                "name": "get_weather",
                "arguments": '{"city": "San Francisco"}'
            }
        }
    ]
}

# Tool result
content = {
    "role": "tool",
    "tool_call_id": "call_123", 
    "name": "get_weather",
    "content": '{"temperature": 72, "condition": "sunny"}'
}
```

<!-- ----------------------- USAGE PATTERNS ---------------------------------- -->

## Usage Patterns

### Basic Session Management

```python
from dasshh.data.client import DBClient
from dasshh.data.session import SessionService

# Initialize
db_client = DBClient()
session_service = SessionService(db_client)

# Create new session
session = session_service.new_session("My first chat")

# Add user message
session_service.add_event(
    invocation_id="inv_123",
    session_id=session.id,
    content={"role": "user", "content": "Hello"}
)

# Add assistant response
session_service.add_event(
    invocation_id="inv_123", 
    session_id=session.id,
    content={"role": "assistant", "content": "Hi there!"}
)
```

### Loading Conversation History

```python
# Get recent session
recent = session_service.get_recent_session()

# Get all events for reconstruction
if recent:
    events = session_service.get_events(session_id=recent.id)
    for event in events:
        print(f"{event.content['role']}: {event.content['content']}")
```
