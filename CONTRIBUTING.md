# Contributing to dasshh

Thank you for your interest in contributing to dasshh! 🎉

This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/dasshh.git
   cd dasshh
   ```

## Development Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create and activate virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   uv sync
   ```

4. **Running the application**:
   ```bash
   python -m dasshh
   ```

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `feature/feature-name` - New features
- `bugfix/issue-description` - Bug fixes
- `docs/update-description` - Documentation updates

### Making Changes

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the project conventions

3. **Run tests locally**:
   ```bash
   pytest -v --cov=dasshh --cov-report=html
   ```

4. **Run linting** (if configured):
   ```bash
   uv pip install ruff
   ruff check .
   ruff format .
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

### Commit Message Convention

We follow conventional commit format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Examples:
```
feat: add new command for file analysis
fix: resolve issue with terminal output formatting
docs: update installation instructions
test: add unit tests for config parser
```

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_should_parse_config_when_valid_file_provided`
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies

Example test structure:
```python
def test_should_process_command_when_valid_input_provided():
    # Arrange
    command = "test command"
    expected_result = "processed"
    
    # Act
    result = process_command(command)
    
    # Assert
    assert result == expected_result
```

## Code Style

### Python Style Guidelines

- Follow [PEP 8](https://pep8.org/)
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions small and focused
- Use descriptive variable names

## Pull Request Process

1. **Ensure your branch is up to date**:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Push your branch**:
   ```bash
   git push origin your-feature-branch
   ```

3. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference any related issues
   - Include screenshots/demos if relevant
   - Ensure all CI checks pass

4. **Address review feedback** promptly and respectfully

5. **Squash commits** if requested before merging

## Issue Reporting

When reporting issues, please include:

- **Environment details**: OS, Python version, dasshh version
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** or logs
- **Screenshots** if relevant

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
uv pip install mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## Getting Help

- Check the [documentation](https://blog.vgnshiyer.dev/dasshh)
- [Open an issue](https://github.com/vgnshiyer/dasshh/issues) for bugs
- [Start a discussion](https://github.com/vgnshiyer/dasshh/discussions) for questions
- Contact maintainers at vgnshiyer@gmail.com or via [LinkedIn](https://www.linkedin.com/in/vgnshiyer/)

## Recognition

Contributors will be acknowledged in:
- Release notes
- GitHub contributors page

Thank you for contributing to dasshh!