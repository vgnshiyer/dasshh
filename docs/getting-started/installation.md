# Installation

Dasshh can be installed on MacOS, Linux and Windows using various package managers. Choose the one that works best for you.

## Using `uv` (Recommended)

If you haven't tried [uv](https://github.com/astral-sh/uv) yet, it's one of those *"I will rewrite this in rust"* projects that is actually awesome. Highly recommend trying it out.

You can install `uv` using `brew` if you are on macOS:

```bash
# Install uv on macOS
brew install uv
```

Or using `curl`.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install `dasshh` using `uv`:

```bash
uv tool install dasshh
```

## Using `pipx`

You can also use [pipx](https://pypa.github.io/pipx/) to install Dasshh.

```bash
# Install pipx if you haven't already
pip install --user pipx
pipx ensurepath

# Install dasshh with pipx
pipx install dasshh
```

## Verifying Installation

After installation, you should be able to run Dasshh from your terminal:

```bash
dasshh --version
```

If the installation was successful, you should see the version of Dasshh printed to the terminal.
