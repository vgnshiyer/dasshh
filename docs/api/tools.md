# Tools

This page lays out all the components available in the tools module.

!!! tip
    Tools are the core mechanism for extending Dasshh's capabilities. Use the `@tool` decorator to convert functions into tools that the AI assistant can use.

<!-- ----------------------- BASETOOL CLASS ---------------------------------- -->

## BaseTool

Abstract base class for all tools in Dasshh.

### `attr` name

The name of the tool

```python
name: str
```

### `attr` description

The description of the tool

```python
description: str
```

### `attr` parameters

The parameters of the tool

```python
parameters: dict
```

### `method` __init__

```python
__init__(name: str, description: str, parameters: dict)
```

Initialize a new BaseTool instance

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| name | | The name of the tool |
| description | | The description of what the tool does |
| parameters | | Dictionary containing the tool's parameters |

### `method` __call__

```python
__call__(*args, **kwargs)
```

Execute the tool with the given arguments

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| *args | | Positional arguments to pass to the tool |
| **kwargs | | Keyword arguments to pass to the tool |

**Raises:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| NotImplementedError | | If the tool has no implementation |

### `method` get_declaration

```python
get_declaration() -> dict
```

Get the declaration of the tool for the AI model

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| dict | | Tool declaration formatted for the AI model |

**Raises:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| NotImplementedError | | If the tool has no implementation |

<!-- ----------------------- FUNCTIONTOOL CLASS ---------------------------------- -->

## FunctionTool

A concrete implementation of BaseTool that wraps Python functions.

### `attr` func

The function wrapped by this tool

```python
func: Callable = None
```

### `method` __init__

```python
__init__(name: str, description: str, parameters: dict, func: Callable = None)
```

Initialize a new FunctionTool instance

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| name | | The name of the tool |
| description | | The description of what the tool does |
| parameters | | Dictionary containing the tool's parameters |
| func | None | The callable function to wrap |

### `method` __call__

```python
__call__(*args, **kwargs)
```

Execute the wrapped function with the given arguments

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| *args | | Positional arguments to pass to the function |
| **kwargs | | Keyword arguments to pass to the function |

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| Any | | The return value of the wrapped function |

**Raises:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| NotImplementedError | | If no function is set |

### `method` get_declaration

```python
get_declaration() -> dict
```

Get the declaration of the tool formatted for the AI model

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| dict | | Tool declaration using litellm's function_to_dict format |

<!-- ----------------------- TOOL DECORATOR ---------------------------------- -->

## @tool Decorator

The main decorator for creating tools in Dasshh.

### `decorator` tool

```python
@tool
def your_function():
    pass
```

Convert a function into a tool and register it with Dasshh

**Usage:**

```python
from dasshh.core.tools.decorator import tool
from typing import Dict

@tool
def hello_world(name: str = "World") -> Dict:
    """
    A simple greeting tool.
    
    Args:
        name (str, optional): The name to greet. Defaults to "World".
        
    Returns:
        Dict: A dictionary containing the greeting message.
    """
    return {"message": f"Hello, {name}!"}
```

**Parameters:**

| Param | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| func | | The function to convert into a tool |

**Returns:**

| Type | <div style="width: 100px">Default</div> | Description |
| ------------- | :----------------: | :----------------------------------------------------------------------------------------|
| FunctionTool | | A FunctionTool instance wrapping the original function |

**Notes:**

- The decorator automatically extracts the function name as the tool name
- The function's docstring becomes the tool description
- Function annotations are used to define tool parameters
- The tool is automatically registered with the global Registry

!!! tip
    Checkout this [guide](../guide/own-tools.md) to build your own tools.
