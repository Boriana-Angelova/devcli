from __future__ import annotations

from pathlib import Path
from typing import List

import typer

from .runner import Runner
from .parser import TracebackParser
from .analyzer import RuleBasedFailureAnalyzer
from .reporter import MarkdownReporter

app = typer.Typer(help="devcli — lightweight python static analysis CLI")

# ------------------------------
# 1️⃣ Static AST analysis
# ------------------------------
@app.command()
def analyze(paths: List[str] = typer.Argument(..., help="Files or directories to analyze")) -> None:
    """Analyze one or more Python files or directories (static AST analysis)."""
    from .runner import run  # твоята стара функция run за AST анализ
    from pathlib import Path

    pths = [Path(p) for p in paths]
    run(pths)


# ------------------------------
# 2️⃣ Runtime failure analysis
# ------------------------------
@app.command(name="run")
def run_command(paths: List[str] = typer.Argument(..., help="Python files to execute and analyze failures")) -> None:
    """Execute Python files, capture exceptions, analyze and report."""
    for path_str in paths:
        path = Path(path_str)
        typer.echo(f"Running {path}...")

        # 1️⃣ Execute file
        runner = Runner()
        result = runner.run([str(path)])

        if result.exit_code != 0:
            # 2️⃣ Parse traceback
            parser = TracebackParser()
            failure_info = parser.parse(result.stderr)

            # 3️⃣ Analyze failure
            analyzer = RuleBasedFailureAnalyzer()
            analysis = analyzer.analyze(failure_info)

            # 4️⃣ Generate Markdown report
            reporter = MarkdownReporter()
            reporter.generate(result, analysis)

            typer.echo(f"Analysis complete for {path}: {analysis.root_cause}")
            typer.echo(f"Suggested fix: {analysis.fix_hint}")
            typer.echo(f"Confidence: {analysis.confidence:.2f}")
        else:
            typer.echo(f"{path} ran successfully ✅")


if __name__ == "__main__":
    app()
