# Dasshh Documentation

This directory contains the documentation for the Dasshh project, built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Running the documentation locally

```bash
# Install dependencies
uv pip install mkdocs-material

# Serve the documentation
mkdocs serve
```

Then visit [http://localhost:8000](http://localhost:8000) in your browser.

## Building the documentation

```bash
mkdocs build
```

This will create a `site` directory with the static HTML files.

## Deploying the documentation

The documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch.

You can also manually deploy the documentation by running:

```bash
mkdocs gh-deploy
``` 