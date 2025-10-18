<div align="center">

# cpc-tree

[![codecov](https://codecov.io/github/ashkonf/cpc-tree/graph/badge.svg?token=7Y596J8IYZ)](https://codecov.io/github/ashkonf/cpc-tree)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Pytest](https://img.shields.io/badge/pytest-✓-brightgreen)](https://docs.pytest.org)
[![Pyright](https://img.shields.io/badge/pyright-✓-green)](https://github.com/microsoft/pyright)
[![Ruff](https://img.shields.io/badge/ruff-✓-blue?logo=ruff)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Build Status](https://img.shields.io/github/actions/workflow/status/ashkonf/cpc-tree/ci.yml?branch=main)](https://github.com/ashkonf/cpc-tree/actions/workflows/ci.yml?query=branch%3Amain)

A Python utility for processing and structuring Cooperative Patent Classification (CPC) data. This tool transforms raw CPC classification XML files into accessible Python data structures and JSON output, making it easy to work with patent classification hierarchies programmatically.

</div>

## Table of Contents

- [Overview](#overview)
- [Dependencies](#dependencies)
- [Usage](#usage)
  - [Setup](#setup)
  - [Download Prerequisite Data](#download-prerequisite-data)
  - [Build the CPC Tree via the CLI](#build-the-cpc-tree-via-the-cli)
  - [Build the CPC Tree in Code](#build-the-cpc-tree-in-code)
  - [Load the CPC Tree in Code](#load-the-cpc-tree-in-code)
  - [Jupyter Notebook](#jupyter-notebook)
- [Data Structure Breakdown](#data-structure-breakdown)
- [API Reference](#api-reference)
  - [Functions](#functions)
  - [Classes](#classes)
- [Development](#development)
  - [Setup](#setup-1)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
  - [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Cooperative Patent Classification (CPC) system is a hierarchical classification scheme used by patent offices worldwide. `cpc-tree` simplifies working with this data by:

- Converting distributed XML classification files into structured Python objects
- Providing both dictionary-based and object-oriented interfaces for navigation
- Exporting classification hierarchies to JSON for use in other applications
- Enabling programmatic access to CPC data for patent analysis workflows

## Dependencies

- Python ≥ 3.11
- `uv` package manager

## Usage

### Setup

First clone this repository:

```bash
git clone https://github.com/ashkonf/cpc-tree.git
cd cpc-tree
```

Then install dependencies:

```bash
uv sync
```

### Download Prerequisite Data

Download and decompress [CPCSchemeXML202508.zip](https://www.cooperativepatentclassification.org/sites/default/files/cpc/bulk/CPCSchemeXML202508.zip) in the repo directory.

### Build the CPC Tree via the CLI

```bash
uv run python -m src.cpc_tree /path/to/xml/directory
```

This will generate a `cpc_tree.json` file containing the complete CPC hierarchy.

### Build the CPC Tree in Code

```python
from src.cpc_tree import build_cpc_tree

# Parse XML files and build dictionary tree
cpc_tree_data = build_cpc_tree("CPCSchemeXML202508")

# Access classification data
print(cpc_tree_data["A"]["title"])  # "HUMAN NECESSITIES"
print(cpc_tree_data["A"]["children"]["A01"]["title"])  # "AGRICULTURE"
```

This will also generate the same `cpc_tree.json` file.

### Load the CPC Tree in Code

```python
from cpc_tree import build_cpc_tree, load_cpc_tree

# Build and convert to CPCTreeNode objects
cpc_tree_data = build_cpc_tree("CPCSchemeXML202508")
cpc_tree = load_cpc_tree(cpc_tree_data)

# Navigate using object interface
root_node = cpc_tree["A"]
print(f"Code: {root_node.code}")  # "A"
print(f"Title: {root_node.title}")  # "HUMAN NECESSITIES"

# Access children
agriculture_node = root_node.children["A01"]
print(f"Agriculture: {agriculture_node.title}")  # "AGRICULTURE"
```

### Jupyter Notebook

For an interactive overview of the steps above in code, see the [sample_usage.ipynb](examples/sample_usage.ipynb) notebook.

## Data Structure Breakdown

The CPC tree follows a hierarchical structure:

```
Section (e.g., "A" - Human Necessities)
├── Class (e.g., "A01" - Agriculture)
│   ├── Subclass (e.g., "A01B" - Soil Working)
│   │   ├── Group (e.g., "A01B1/00" - Hand Tools)
│   │   │   └── Subgroup (e.g., "A01B1/02" - Spades, Shovels)
```

Each node contains:
- `code`: Classification symbol (e.g., "A01B1/02")
- `title`: Human-readable description
- `children`: Dictionary of child nodes

## API Reference

### Functions

#### `build_cpc_tree(directory: str) -> Dict[str, Any]`

Builds the complete CPC tree from XML files in the specified directory.

**Parameters:**
- `directory`: Path to directory containing [CPCSchemeXML202508.zip](https://www.cooperativepatentclassification.org/sites/default/files/cpc/bulk/CPCSchemeXML202508.zip).

**Returns:** Dictionary representation of the CPC hierarchy

#### `load_cpc_tree(data: Dict[str, Any]) -> Dict[str, CPCTreeNode]`

Converts dictionary representation to CPCTreeNode objects for easier navigation.

**Parameters:**
- `data`: Dictionary tree from `build_cpc_tree()` or loaded JSON

**Returns:** Dictionary mapping codes to CPCTreeNode objects

### Classes

#### `CPCTreeNode`

Represents a single node in the CPC classification tree.

**Attributes:**
- `code: str` - Classification symbol
- `title: Optional[str]` - Human-readable title
- `children: Dict[str, CPCTreeNode]` - Child nodes

## Development

### Setup

```bash
# Clone and install with development dependencies
git clone https://github.com/ashkonf/cpc-tree.git
cd cpc-tree
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

First download and decompress [CPCSchemeXML202508.zip](https://www.cooperativepatentclassification.org/sites/default/files/cpc/bulk/CPCSchemeXML202508.zip) in the repo directory.

Then run:

```bash
uv run python -m pytest
```

### Code Quality

This project uses several tools for code quality:

```bash
# Linting and formatting
uv run ruff check --fix
uv run ruff format

# Type checking
uv run pyright

# Run all checks (via pre-commit)
uv run pre-commit run --all-files
```

### Project Structure

```
cpc-tree/
├── cpc_tree/            # Package containing logic and CLI
│   ├── __init__.py      # Core processing logic
│   └── __main__.py      # Command line entry point
├── tests/
│   └── test_cpc_tree.py # Test suite
├── cpc_tree.json        # Generated CPC hierarchy (large file)
├── pyproject.toml       # Project configuration
├── uv.lock             # Locked dependencies
├── .pre-commit-config.yaml  # Code quality hooks
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b username/amazing-feature`
3. Make your changes
4. Run tests and quality checks: `uv run pre-commit run --all-files`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request against `main`

## License

This project is licensed under the Apache License, Version 2.0. See the `LICENSE` file for more details.
