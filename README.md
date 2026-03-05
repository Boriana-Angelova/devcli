# devcli

A small, production-ready Python CLI for light static analysis of Python files.

Quick start

Install (recommended via virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

Example usage

```bash
# Analyze a single file
devcli analyze path/to/module.py

# Analyze multiple files or directories
devcli analyze src/ tests/other.py
```

Project layout

- `cli.py` - top-level Typer entrypoint
- `devcli/` - package containing core modules: `runner.py`, `parser.py`, `analyzer.py`, `reporter.py`, `ast_utils.py`, `models.py`
