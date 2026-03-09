from __future__ import annotations

import tempfile
import subprocess
from pathlib import Path
from typing import List

import typer

from devcli.runner import Runner, run


app = typer.Typer(help="devcli — lightweight Python static & runtime analysis CLI")


# --------------------------------
# Helper: clone GitHub repository
# --------------------------------
def clone_repo(repo_url: str) -> Path:
    """Clone a Git repository to a temporary directory."""
    temp_dir = Path(tempfile.mkdtemp())

    subprocess.run(
        ["git", "clone", repo_url, str(temp_dir)],
        check=True,
    )

    return temp_dir


# --------------------------------
# Static AST analysis
# --------------------------------
@app.command()
def analyze(
    paths: List[str] = typer.Argument(..., help="Files, directories, or GitHub repositories"),
) -> None:
    """Perform static AST analysis on Python files or repositories."""

    resolved_paths: List[Path] = []

    for p in paths:
        if p.startswith("http://") or p.startswith("https://"):
            typer.echo(f"Cloning repository: {p}")
            repo_path = clone_repo(p)
            resolved_paths.append(repo_path)
        else:
            resolved_paths.append(Path(p))

    run(resolved_paths)


# --------------------------------
# Runtime failure analysis
# --------------------------------
@app.command()
def runfiles(
    paths: List[str] = typer.Argument(..., help="Python files to execute and analyze failures"),
) -> None:
    """Execute Python files, capture exceptions, and analyze failures."""

    for path_str in paths:
        path = Path(path_str)
        typer.echo(f"Running {path}...")

        runner = Runner()
        result = runner.run([str(path)])

        if result.exit_code != 0:
            typer.echo("Failure detected. Analyzing...")

            # Parse traceback
            parser = TracebackParser()
            failure_info = parser.parse(result.stderr)

            # Analyze root cause
            analyzer = RuleBasedFailureAnalyzer()
            analysis = analyzer.analyze(failure_info)

            # Generate report
            reporter = MarkdownReporter()
            reporter.generate(result, analysis)

            typer.echo(f"Root cause: {analysis.root_cause}")
            typer.echo(f"Suggested fix: {analysis.fix_hint}")
            typer.echo(f"Confidence: {analysis.confidence:.2f}")

        else:
            typer.echo(f"{path} ran successfully ✅")


if __name__ == "__main__":
    app()