# Build your own tools

Dasshh allows you to extend its capabilities by creating your own custom tools. This guide will walk you through the process of building, testing, and integrating your own tools into Dasshh.

## Tool basics

In Dasshh, a tool is a Python function decorated with the `@tool` decorator. When you create a tool, it's automatically registered with Dasshh's tool registry, making it available for the AI assistant to use in conversations.

## Creating a simple tool

Let's create a simple "hello world" tool to understand the basics:

1. Create a new Python file in your desired location (we'll use a custom directory for this example)
2. Define a function with proper type annotations and docstring
3. Decorate it with the `@tool` decorator

Here's an example:

```python
from dasshh.core.tools.decorator import tool
from typing import Dict

@tool
def hello_world(name: str = "World") -> Dict:
    """
    A simple greeting tool that says hello to the provided name.
    
    Args:
        name (str, optional): The name to greet. Defaults to "World".
        
    Returns:
        Dict: A dictionary containing the greeting message.
    """
    return {
        "message": f"Hello, {name}!"
    }
```

!!! note
    Functions must return a python dictionary.

## Tool components

Every tool can have the following components:

1. **Function Name**: This becomes the tool's name in the registry (e.g., `hello_world`)
2. **Docstring**: This becomes the tool's description, explaining what it does
3. **Type Annotations**: Define the input parameters and return type
4. **Implementation**: The actual code that executes when the tool is called

## Setting up your custom tools directory

To organize your custom tools, it's best to create a dedicated directory structure like this:

```
my_dasshh_tools/
├── __init__.py
└── weather/
    ├── __init__.py
    └── weather_tools.py
```

### Step 1: Create your directory structure

```bash
mkdir -p my_dasshh_tools/weather
touch my_dasshh_tools/__init__.py
touch my_dasshh_tools/weather/__init__.py
```

### Step 2: Create your tool files

For example, in `my_dasshh_tools/weather/weather_tools.py`:

```python
from typing import Dict
from dasshh.core.tools.decorator import tool

@tool
def get_weather(city: str) -> Dict:
    """
    Get the current weather for a specified city.
    
    Args:
        city (str): The name of the city
        
    Returns:
        Dict: Weather information for the specified city
    """
    if city == "San Francisco":
        return {
            "temperature": 15,
            "description": "sunny"
        }
    else:
        return {
            "temperature": None,
            "description": "Weather not available for this city"
        }
```

### Step 3: Import your tools in the `__init__.py` files

In `my_dasshh_tools/weather/__init__.py`:

```python
from .weather_tools import get_weather

__all__ = ['get_weather']
```

In `my_dasshh_tools/__init__.py`:

```python
from . import weather

__all__ = ['weather']
```

## Registering your tools with Dasshh

To make your tools available to Dasshh, you need to add your custom directory to Dasshh's configuration.

1. Open your Dasshh configuration file at `~/.dasshh/config.yaml`
2. Add your custom directory to the `tool_directories` list.

```yaml
dasshh:
  skip_summarization: false
  system_prompt: |
    You are a helpful assistant that can help with tasks on the system.
  tool_directories:
    - /path/to/dasshh/apps         # Default tools directory
    - /path/to/my_dasshh_tools     # Your custom tools directory
```

## Tool design best practices

When creating your tools, follow these best practices:

1. **Clear Names**: Use descriptive function names that indicate what the tool does
2. **Detailed Docstrings**: Write clear descriptions of what the tool does, including parameter explanations
3. **Proper Type Annotations**: Use Python type hints for all parameters and return values
4. **Error Handling**: Handle exceptions gracefully and return informative error messages
5. **Return Structured Data**: Always return dictionaries or similar structured data that's easy to parse
6. **Keep It Focused**: Each tool should do one thing well rather than many things

## Testing tool discovery

To test if your tools are being discovered, ask Dasshh to list all tools.

```
List all available tools
```

If you see your tools listed, you're good to go!

## Debugging your tools

If your tool isn't working as expected within Dasshh:

1. Check the Dasshh logs at `~/.dasshh/logs/dasshh.log`
2. Ensure your tool directory is correctly listed in the configuration
3. Verify that your tool is being imported correctly
4. Check that your function signatures and type annotations are correct

## Understanding how tools are registered

When you decorate a function with `@tool`, the following happens:

1. A `FunctionTool` instance is created with the function's name, docstring, and type annotations
2. This tool is added to the global `Registry`
3. When Dasshh starts, it scans all directories listed in `tool_directories` and imports them
4. During import, the decorators run and register all tools
5. The assistant can then access this registry to use the tools

Now you're ready to create your own custom tools for Dasshh!

## Additional Resources

- [Function Calling best practices (OpenAI)](https://platform.openai.com/docs/guides/function-calling?api-mode=responses)
