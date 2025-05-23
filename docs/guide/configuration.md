# Configuration

Below is a list of available configuration options.

## Initial Setup

The default configuration file is located at `~/.dasshh/config.yaml`.

Below command helps you initialize the configuration file.

```bash
dasshh init-config
```

## Configuration Options

### Dasshh Configuration

| Option | Description |
|--------|-------------|
| `skip_summarization` | Skip summarization of tool call results |
| `system_prompt` | The system prompt for the assistant |
| `tool_directories` | The directories to search for tools |

### Model Configuration

| Option | Description |
|--------|-------------|
| `model.name` | The model provider and model name |
| `model.api_key` | Your API key for the chosen provider |
| `model.api_base` | The base URL for the chosen provider |
| `model.api_version` | The version of the API to use |
| `model.temperature` | The temperature for the model |
| `model.top_p` | The top-p value for the model |
| `model.max_tokens` | The maximum number of tokens to generate |
| `model.max_completion_tokens` | The maximum number of tokens to generate for the completion |

## Example Configuration File

The configuration file is a YAML file with the following structure.

```yaml
# Dasshh configuration
dasshh:
  skip_summarization: false
  system_prompt: |
    You are a helpful assistant that can help with tasks on the system.
    Your goal is to save user's time by performing tasks on their behalf.
  tool_directories:
    - /Users/viiyer/repos/dasshh/dasshh/apps

# Model configuration
model:
  name: gemini/gemini-2.0-flash
  api_base:
  api_key: <your-google-AI-studio-api-key>
  api_version:
  temperature: 1.0
  top_p: 1.0
  max_tokens: 1000
  max_completion_tokens: 1000
```

## Supported Models

Dasshh supports a variety of models through [LiteLLM](https://docs.litellm.ai/docs/providers).

### Format for specifying a model

```yaml
model:
  name: <provider>/<model-name>
  api_key: <your-api-key>
```