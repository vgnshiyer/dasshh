# Testing Dasshh

This directory contains tests for Dasshh.

## Structure

- `unit/`: Unit tests for individual components
  - `core/`: Tests for core functionality
  - `ui/`: Tests for UI components
  - `apps/`: Tests for application modules
  - `data/`: Tests for data models and storage

## Running Tests

To run all tests:

```bash
python -m pytest
```

To run tests with coverage:

```bash
python -m pytest --cov=dasshh
```

To generate a coverage report:

```bash
python -m pytest --cov=dasshh --cov-report=html
```

This will create a directory called `htmlcov` with an HTML report of the coverage.

## Adding Tests

When adding new functionality, please add corresponding tests. Test files should follow the naming convention `test_*.py` and test functions should be named `test_*`. 