from collections import namedtuple

# -- return types for runtime -- #

Query = namedtuple(
    "Query",
    [
        "invocation_id",
        "session_id",
        "text",
    ]
)

AssistantResponse = namedtuple(
    "AssistantResponse",
    [
        "text",
        "is_complete",
        "is_partial"
    ]
)

# -- return types for session service -- #

Session = namedtuple(
    "Session",
    [
        "id",
        "detail",
        "last_updated_at",
        "messages",
        "tools"
    ]
)

Message = namedtuple(
    "Message",
    [
        "id",
        "role",
        "text",
        "timestamp",
    ]
)

ToolCall = namedtuple(
    "ToolCall",
    [
        "id",
        "name",
        "args",
        "timestamp",
    ]
)

ToolCallResult = namedtuple(
    "ToolCallResult",
    [
        "id",
        "name",
        "result",
        "timestamp",
    ]
)
