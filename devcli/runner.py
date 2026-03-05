from __future__ import annotations

import logging
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from . import parser, reporter

logger = logging.getLogger("devcli")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


@dataclass
class RunResult:
    command: str
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float


class Runner:
    """Utility to execute shell commands and capture results.

    Usage:
        r = Runner(shell=False)
        result = r.run(["ls", "-la"], timeout=5)
    """

    def __init__(self, *, shell: bool = False) -> None:
        self.shell = shell

    def run(self, cmd: str | List[str], timeout: float | None = None) -> RunResult:
        """Execute `cmd` and return a `RunResult`.

        Args:
            cmd: command string or list of args.
            timeout: seconds before timing out (None = no timeout).
        """
        start = time.monotonic()
        cmd_display = cmd if isinstance(cmd, str) else " ".join(cmd)
        try:
            completed = subprocess.run(
                cmd,
                shell=self.shell,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            end = time.monotonic()
            return RunResult(
                command=cmd_display,
                stdout=completed.stdout or "",
                stderr=completed.stderr or "",
                exit_code=completed.returncode,
                execution_time=end - start,
            )
        except subprocess.TimeoutExpired as ex:
            end = time.monotonic()
            stdout = ex.stdout or ""
            stderr = ex.stderr or f"Command timed out after {timeout} seconds"
            return RunResult(
                command=cmd_display,
                stdout=stdout,
                stderr=stderr,
                exit_code=-1,
                execution_time=end - start,
            )
        except Exception as ex:  # pragma: no cover - unexpected errors
            end = time.monotonic()
            return RunResult(
                command=cmd_display,
                stdout="",
                stderr=str(ex),
                exit_code=-2,
                execution_time=end - start,
            )


IGNORE_DIRS = {"venv", ".venv", "__pycache__", ".git", "site-packages"}


def _gather_python_files(paths: Iterable[Path]) -> List[Path]:
    files: List[Path] = []

    for p in paths:
        if p.is_dir():
            for child in p.rglob("*.py"):
                # ignore unwanted directories
                if any(part in IGNORE_DIRS for part in child.parts):
                    continue
                files.append(child)

        elif p.is_file() and p.suffix == ".py":
            files.append(p)

        else:
            logger.debug("Skipping non-python path: %s", p)

    return sorted(set(files))


def run(paths: Iterable[Path]) -> int:
    """Run the analysis pipeline on the provided paths.

    Returns an exit code (0 on success, >0 on error).
    """
    files = _gather_python_files(paths)
    if not files:
        logger.error("No Python files found in given paths")
        return 2

    analyses = []
    for f in files:
        try:
            a = parser.parse_file(f)
            analyses.append(a)
        except Exception as exc:  # pragma: no cover - top-level robust handling
            logger.error("Failed to parse %s: %s", f, exc)

    out = reporter.report(analyses)

   # Save report to Markdown file
    output_path = Path("analysis_report.md")
    output_path.write_text(out, encoding="utf-8")

    print(out)
    print(f"\nReport saved to {output_path}")

    return 0
