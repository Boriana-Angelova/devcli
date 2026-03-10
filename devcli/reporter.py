from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .models import FileAnalysis, FailureInfo, RunResult, AnalysisResult


def report(analyses: Iterable[FileAnalysis]) -> str:
    """Render a concise multi-file report as plain text."""
    lines: list[str] = []
    total_files = 0
    total_funcs = 0
    total_classes = 0
    total_todos = 0

    for a in analyses:
        total_files += 1
        total_funcs += len(a.functions)
        total_classes += len(a.classes)
        total_todos += a.todo_count
        lines.append(f"{a.path} — functions={len(a.functions)} classes={len(a.classes)} todos={a.todo_count}")

    lines.append("")
    lines.append(f"TOTAL files={total_files} functions={total_funcs} classes={total_classes} todos={total_todos}")
    return "\n".join(lines)


@dataclass
class RuleResult:
    rule: str
    root_cause: str
    suggestion: str
    confidence: float


class MarkdownReporter:
    """Generate a structured Markdown report for a run + analysis."""

    def __init__(self, out_path: Path | str = "failure_report.md") -> None:
        self.out_path = Path(out_path)

    def generate(self, run_result: RunResult, analysis: AnalysisResult) -> str:
        lines: List[str] = []
        lines.append(f"# Failure Report\n")
        lines.append("## Command\n")
        lines.append(f"`{run_result.command}`\n")
        lines.append("## Execution\n")
        lines.append(f"- Exit code: **{run_result.exit_code}**")
        lines.append(f"- Execution time: **{run_result.execution_time:.3f}s**\n")

        lines.append("### Stdout\n")
        lines.append("```\n" + (run_result.stdout or "<empty>") + "\n```")
        lines.append("### Stderr\n")
        lines.append("```\n" + (run_result.stderr or "<empty>") + "\n```")

        lines.append("\n## Exception Details\n")
        f = analysis.failure
        lines.append(f"- Type: **{f.exception_type or '<unknown>'}**")
        lines.append(f"- Message: {f.message or '<none>'}")
        file_loc = f"{f.file}:{f.line}" if f.file else "<unknown>"
        lines.append(f"- Location: {file_loc} in `{f.function or '<unknown>'}`\n")

        # Primary analysis
        primary: RuleResult | None = analysis.rule_results[0] if analysis.rule_results else None
        if primary:
            lines.append("## Root Cause\n")
            lines.append(primary.root_cause + "\n")
            lines.append("## Suggested Fix\n")
            lines.append(primary.suggestion + "\n")
            lines.append(f"**Confidence:** {primary.confidence:.2f}\n")

        if analysis.rule_results:
            lines.append("## All Rules\n")
            for r in analysis.rule_results:
                lines.append(f"- **{r.rule}** (confidence: {r.confidence:.2f}) — {r.root_cause}")

        return "\n".join(lines)

    def generate_and_save(self, run_result: RunResult, analysis: AnalysisResult) -> Path:
        content = self.generate(run_result, analysis)
        self.out_path.write_text(content, encoding="utf-8")
        return self.out_path