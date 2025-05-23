# Contributing to Dasshh

Thank you for your interest in contributing to Dasshh! This guide will help you get started with the development process.

## Setting Up the Development Environment

1. Clone the repository:

```bash
git clone https://github.com/vgnshiyer/dasshh.git
cd dasshh
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:

```bash
uv sync
```

## Running Dasshh in Development Mode

To run Dasshh locally during development:

```bash
python -m dasshh
```

## Development Workflow

1. Create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test them locally.

3. Run the tests to ensure everything works:

```bash
pytest
```

4. Commit your changes with a descriptive message:

```bash
git add .
git commit -m "Add your descriptive message here"
```

5. Push your branch and create a pull request:

```bash
git push origin feature/your-feature-name
```

Then, create a pull request on GitHub.

## Code Style

Dasshh follows the PEP 8 style guide for Python code. Please ensure your code adheres to this standard.

## Testing

All new features should include appropriate test coverage. Run the test suite using:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=dasshh
```

## Documentation

When adding new features, please update the documentation accordingly. Dasshh uses MkDocs for documentation.

To preview the documentation locally:

```bash
mkdocs serve
```

Then visit `http://localhost:8000` in your browser. 