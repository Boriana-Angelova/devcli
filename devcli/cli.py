import tempfile
import subprocess
from pathlib import Path
from typing import List
import typer

from devcli.runner import run


def clone_repo(repo_url: str) -> Path:
    """Clone a Git repository to a temporary directory."""
    temp_dir = Path(tempfile.mkdtemp())

    subprocess.run(
        ["git", "clone", repo_url, str(temp_dir)],
        check=True,
    )

    return temp_dir


app = typer.Typer(help="devcli — lightweight python static analysis CLI")


@app.command()
def analyze(
    paths: List[str] = typer.Argument(..., help="Paths or GitHub repos"),
) -> None:
    """Analyze local paths or GitHub repositories."""

    resolved_paths: List[Path] = []

    for p in paths:
        if p.startswith("http://") or p.startswith("https://"):
            typer.echo(f"Cloning repository: {p}")
            repo_path = clone_repo(p)
            resolved_paths.append(repo_path)
        else:
            resolved_paths.append(Path(p))

    run(resolved_paths)


if __name__ == "__main__":
    app()