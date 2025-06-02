# Configuration

Below is a list of available configuration options.

## Initial Setup

The default configuration file is located at `~/.dasshh/config.yaml`.

Below command helps you initialize the configuration file.

```bash
dasshh init-config
```

!!! note "Automatic Migration"
    If you have an existing configuration file with the old `model:` format, Dasshh will automatically migrate it to the new format when you start the application.

## Configuration Options

### Dasshh Configuration

| Option | Description |
|--------|-------------|
| `skip_summarization` | Skip summarization of tool call results |
| `system_prompt` | The system prompt for the assistant |
| `theme` | The theme to use for the UI |
| `tool_directories` | The directories to search for tools |
| `selected_model` | The currently selected model name from your configured models |

### Models Configuration

The `models` section allows you to configure multiple AI models.

Each model entry has the following structure:

| Option | Description |
|--------|-------------|
| `model_name` | A unique identifier for this model configuration |
| `litellm_params` | Model specific configurations (litellm compatible) |

!!! note
    Visit [LiteLLM documentation](https://docs.litellm.ai/docs/proxy/configs) to see the complete list of supported parameters.

## Example Configuration File

The configuration file is a YAML file with the following structure.

```yaml
# Dasshh configuration
dasshh:
  skip_summarization: false
  system_prompt: |
    You are a helpful assistant that can help with tasks on the system.
    Your goal is to save user's time by performing tasks on their behalf.
  theme: lime
  tool_directories:
    - /Users/viiyer/repos/dasshh/dasshh/apps
  selected_model: gemini-flash

# Models configuration - you can configure multiple models
models:
  - model_name: gemini-flash  # Human readable name for the model
    litellm_params:
      model: gemini/gemini-2.0-flash
      api_key: <your-google-AI-studio-api-key>
      temperature: 1.0
      top_p: 1.0
      max_tokens: 1000
      max_completion_tokens: 1000
      
  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_key: <your-openai-api-key>
      temperature: 0.7
      max_tokens: 2000
      
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: <your-anthropic-api-key>
      temperature: 0.8
```

## Multi-Model Support

You can configure multiple models and switch between them:

1. **Configure models** - Add multiple model configurations in the `models` array
2. **Select active model** - Set `dasshh.selected_model` to the `model_name` of your choice
3. **Switch models** - Use `Ctrl+P` in the UI to quickly switch between configured models
4. **Manage in UI** - Use the Settings panel to add, edit, or configure models with a visual interface

## Supported Models

Dasshh supports a variety of models through [LiteLLM](https://docs.litellm.ai/docs/providers).

### Format for specifying a model

```yaml
models:
  - model_name: my-custom-name
    litellm_params:
      model: <provider>/<model-name>
      api_key: <your-api-key>
      # ... other parameters
```