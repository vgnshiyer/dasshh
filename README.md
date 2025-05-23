<div align="center">

# 🗲 &nbsp; *Dasshh* &nbsp; 🗲

***An AI Agent on your terminal, to preserve your brain juice.***

Dasshh is a tui built with [textual](https://textual.textualize.io/) that allows you to interact with your computer using natural language.

</div>

<hr>

[![PyPI](https://img.shields.io/pypi/v/dasshh.svg)](https://pypi.org/project/dasshh/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Follow-vgnshiyer-0A66C2?logo=linkedin)](https://www.linkedin.com/comm/mynetwork/discovery-see-all?usecase=PEOPLE_FOLLOWS&followMember=vgnshiyer)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow.svg?logo=buymeacoffee)](https://www.buymeacoffee.com/vgnshiyer)

**Note:** This project is still in early development. Suggestions and contributions are welcome!

## ✨ Features 

- Interactive & minimal chat UI
- Chat with your personal assistant on your terminal
- Perform actions on your computer with plain English
- Extensible with your own tools

## 📸 Screenshots

<img src="assets/demo.png" alt="Dasshh Demo" width="800">

## 📦 Installation

### Using `uv` (Recommended)

If you haven't tried [uv](https://github.com/astral-sh/uv) yet, it's highly recommended for fast Python package management.

```bash
# Install uv on macOS
brew install uv

# Or using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dasshh
uv tool install dasshh
```

### Using `pipx`

```bash
# Install pipx if you haven't already
pip install --user pipx
pipx ensurepath

# Install dasshh
pipx install dasshh
```

### Verify Installation

```bash
dasshh --version
```

## 🚀 Quick Start

### 1. Initialize Configuration

```bash
dasshh init-config
```

This creates a config file at `~/.dasshh/config.yaml`.

### 2. Configure Your Model

Edit the config file to set your model and API key:

```yaml
model:
  name: gemini/gemini-2.0-flash
  api_key: <your-google-AI-studio-api-key>
```

> See [litellm docs](https://docs.litellm.ai/docs/providers) for all supported models and providers.

### 3. Launch Dasshh

```bash
dasshh
```

### 4. Start Chatting

Ask Dasshh to help with system tasks:

```
• What's the current CPU usage?
• Show me the top memory-intensive processes  
• List files in my downloads folder
• Create a new directory called "projects"
```

**Exit:** Press `Ctrl+C` to terminate.

## 📖 Documentation

The documentation is available at [https://vgnshiyer.github.io/dasshh/](https://vgnshiyer.github.io/dasshh/).

### Running the docs locally

```bash
# Install dependencies
uv pip install mkdocs-material

# Serve the documentation
mkdocs serve
```

Then visit [http://localhost:8000](http://localhost:8000) in your browser.

## 🤝 Contributing

Contributions are welcome! Please open an issue with your suggestions or feature requests.

## 🛠️ Development

### Clone the repository

```bash
git clone https://github.com/vgnshiyer/dasshh.git
cd dasshh
```

### Install dependencies

```bash
uv sync
```

### Run the app

```bash
python -m dasshh
```

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

