from typing import List
import typer

from devcli.runner import run

app = typer.Typer(help="devcli — lightweight python static analysis CLI")


@app.command()
def analyze(paths: List[str] = typer.Argument(..., help="Files or directories to analyze")) -> None:
    """Analyze one or more Python files or directories."""
    from pathlib import Path

    pths = [Path(p) for p in paths]
    run(pths)


if __name__ == "__main__":
    app()
