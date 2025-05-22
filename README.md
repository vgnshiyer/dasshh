<div align="center">

# 🗲 &nbsp; *Dasshh* &nbsp; 🗲

***An AI Agent on your terminal, to preserve your brain juice.***

Dasshh is a terminal-based AI agent that allows you to interact with your computer using natural language.

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

### Using `uv`

```bash
brew install uv  # macOS
uvx dasshh
```

### Prefer `pipx`?

```bash
pipx install dasshh
```

### Initial Setup

Before running the app, you need to initialize the configuration file:

```bash
dasshh init-config
```

This will create a configuration file at `~/.dasshh/config.yaml`. You need to edit this file to set your API key and other preferences:

```yaml
# Edit the file to set your model API key
model:
  name: gemini/gemini-2.0-flash
  api_key: YOUR_API_KEY_HERE
```

Checkout [litellm docs](https://docs.litellm.ai/docs/providers) for detailed model configuration.

### Running the app

```bash
dasshh
```

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

