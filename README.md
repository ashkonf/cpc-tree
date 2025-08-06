# cpc-tree

A Python utility for processing and structuring Cooperative Patent Classification (CPC) data. This tool transforms raw CPC classification XML files into accessible Python data structures and JSON output, making it easy to work with patent classification hierarchies programmatically.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Using UV (Recommended)](#using-uv-recommended)
  - [Using pip](#using-pip)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
    - [Building the CPC Tree](#building-the-cpc-tree)
    - [Loading the Generated JSON as Objects](#loading-the-generated-json-as-objects)
- [Data Structure](#data-structure)
- [API Reference](#api-reference)
  - [Functions](#functions)
  - [Classes](#classes)
- [Development](#development)
  - [Setup](#setup)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
  - [Project Structure](#project-structure)
- [Contributing](#contributing)

## Overview

The Cooperative Patent Classification (CPC) system is a hierarchical classification scheme used by patent offices worldwide. CPC-Tree simplifies working with this complex data by:

- Converting distributed XML classification files into structured Python objects
- Providing both dictionary-based and object-oriented interfaces for navigation
- Exporting classification hierarchies to JSON for use in other applications
- Enabling programmatic access to CPC data for patent analysis workflows

**Target Users**: Patent researchers, classification analysts, and developers building applications that work with patent classification systems.

## Requirements

- Python ≥ 3.13
- UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/ashkonf/cpc-tree.git
cd cpc-tree

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/ashkonf/cpc-tree.git
cd cpc-tree

# Install dependencies
pip install -e .
```

## Usage

For an interactive introduction, see the [sample_usage.ipynb](examples/sample_usage.ipynb) notebook.

### Command Line Interface

Process CPC XML files from a directory containing the classification scheme:

```bash
# Using UV
uv run python -m cpc_tree /path/to/xml/directory

# Using Python directly
python -m cpc_tree /path/to/xml/directory
```

This will generate a `cpc_tree.json` file containing the complete CPC hierarchy.

**Input Requirements**: The XML directory should contain:
- `cpc-scheme.xml` (main classification file)
- Additional linked XML files referenced by the scheme

### Python API

#### Building the CPC Tree

Download and decompress [CPCSchemeXML202508.zip](https://www.cooperativepatentclassification.org/sites/default/files/cpc/bulk/CPCSchemeXML202508.zip) in the repo directory.

Then run:
```python
from cpc_tree import build_cpc_tree

# Parse XML files and build dictionary tree
cpc_tree_data = build_cpc_tree("CPCSchemeXML202508")

# Access classification data
print(cpc_tree_data["A"]["title"])  # "HUMAN NECESSITIES"
print(cpc_tree_data["A"]["children"]["A01"]["title"])  # "AGRICULTURE"
```

#### Loading the Generated JSON as Objects

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

## Data Structure

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

Download and decompress CPCSchemeXML202508.zip in the repo directory.

Then run:

```bash
# Run all tests
uv run python -m pytest

# Run with verbose output
uv run python -m pytest -v
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
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks (`uv run pre-commit run --all-files`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request




