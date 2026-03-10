Project: devcli – Static Analysis CLI Tool

A small, production-ready Python CLI for light static analysis of Python files.

1. Project Overview
devcli is a modular Python-based static analysis CLI tool designed to analyze Python projects and generate structured diagnostic reports.

2. System Architecture
The system follows a clean modular architecture with separation of concerns:
• CLI Layer (cli.py)
• Execution Layer (runner.py)
• Static Analysis Layer (ast_utils.py, parser.py)
• Parsing Layer (traceback_parser.py), if runtime error detected
• Rule-Based Analysis Engine (analyzer.py, failure_analyzer.py)
• Reporting Layer (reporter.py)
• Data Models (models.py)
• Output: analysis_report.md / failure_report.md

3. Development Approach
The project was developed using an AI-assisted workflow including architecture design, code generation support, refactoring, testing, and debugging.

4. Who This Project Is Useful For
This tool is useful for Python developers, students learning software architecture, teams building internal tools, educators demonstrating modular design, and developers working on CI/CD automation.

5. Conclusion
The devcli project demonstrates AI-assisted software engineering, modular architecture, rule-based reasoning, structured static analysis, and professional Python packaging practices.


How it works?

Quick start

Install (recommended via virtualenv):

```bash
python -m venv .venv
# Linux / Mac:
source .venv/bin/activate   
# on Windows: 
.\.venv\Scripts\activate
# Then install the dependencies:
pip install -r requirements.txt
# Install the project in editable mode:
pip install -e .
```

Example usage

```bash
# Analyze a single file
devcli analyze path/to/module.py

# Analyze multiple files or directories
devcli analyze src/ tests/other.py

# Analyze git repo
devcli analyze https://github.com/path

# Runfiles a single file
devcli runfiles my_file.py
```

Project layout

- `devcli/` - package containing core modules: `cli.py`,`runner.py`, `ast_utils.py`, `parser.py`, `traceback_parser.py`, `analyzer.py`,  `failure_analyzer.py`, `reporter.py`, `models.py`
