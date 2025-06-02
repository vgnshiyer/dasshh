from pathlib import Path
import importlib.resources as pkg_resources


DEFAULT_CONFIG_PATH = Path.home() / ".dasshh" / "config.yaml"
try:
    DASSHH_EXEC_PATH = str(Path(pkg_resources.files("dasshh")))
except (ImportError, TypeError):
    DASSHH_EXEC_PATH = str(Path(__file__).parent.parent)

DEFAULT_TOOLS_PATH = str(Path(DASSHH_EXEC_PATH) / "apps")

DEFAULT_CONFIG = f"""
dasshh:
  skip_summarization: false
  system_prompt:
  tool_directories:
  - {DEFAULT_TOOLS_PATH}
  theme: lime
  selected_model: mymodel

models:
- model_name: mymodel
  litellm_params:
    model:
    base_url:
    api_key:
    api_version:
    temperature: 1.0
    top_p: 1.0
    max_tokens:
    max_completion_tokens:
"""
