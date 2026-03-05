Project: devcli – Static Analysis CLI Tool

A small, production-ready Python CLI for light static analysis of Python files.

1. Project Overview
devcli is a modular Python-based static analysis CLI tool designed to analyze Python projects, parse execution errors, and generate structured diagnostic reports.

2. System Architecture
The system follows a clean modular architecture with separation of concerns:
• CLI Layer (cli.py)
• Execution Layer (runner.py)
• Parsing Layer (traceback_parser.py)
• Rule-Based Analysis Engine (analyzer.py)
• Static Analysis Layer (ast_utils.py)
• Reporting Layer (reporter.py)
• Data Models (models.py)

3. System Execution Flow
The following diagram describes the execution pipeline:

User Command (CLI)
        ↓
CLI Layer (Typer)
        ↓
Execution Layer (Run Command)
        ↓
If Error → Traceback Parser
        ↓
Rule-Based Analysis Engine
        ↓
Report Generator (Markdown)
        ↓
Output to failure_report.md

4. Development Approach
The project was developed using an AI-assisted workflow including architecture design, code generation support, refactoring, testing, and debugging.

5. Who This Project Is Useful For
This tool is useful for Python developers, students learning software architecture, teams building internal tools, educators demonstrating modular design, and developers working on CI/CD automation.

6. Conclusion
The devcli project demonstrates AI-assisted software engineering, modular architecture, rule-based reasoning, structured static analysis, and professional Python packaging practices.


How it works?

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
