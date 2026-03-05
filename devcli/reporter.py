from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from .models import FileAnalysis, FailureInfo


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
class AnalysisResult:
    failure: FailureInfo
    rule_results: List["RuleResult"]


class MarkdownReporter:
    """Generate a structured Markdown report for a run + analysis.

    The report includes command, outputs, exception details, root cause, suggested fix and confidence.
    """

    def __init__(self, out_path: Path | str = "failure_report.md") -> None:
        self.out_path = Path(out_path)

    def generate(self, run_result: "RunResult", analysis: AnalysisResult) -> str:
        lines: List[str] = []
        lines.append(f"# Failure Report")
        lines.append("")
        lines.append("## Command")
        lines.append("")
        lines.append(f"`{run_result.command}`")
        lines.append("")
        lines.append("## Execution")
        lines.append("")
        lines.append(f"- Exit code: **{run_result.exit_code}**")
        lines.append(f"- Execution time: **{run_result.execution_time:.3f}s**")
        lines.append("")
        lines.append("### Stdout")
        lines.append("")
        lines.append("```\n" + (run_result.stdout or "<empty>") + "\n```")
        lines.append("")
        lines.append("### Stderr")
        lines.append("")
        lines.append("```\n" + (run_result.stderr or "<empty>") + "\n```")
        lines.append("")
        lines.append("## Exception Details")
        lines.append("")
        f = analysis.failure
        lines.append(f"- Type: **{f.exc_type or '<unknown>'}**")
        lines.append(f"- Message: {f.message or '<none>'}")
        file_loc = f"{f.file}:{f.line}" if f.file else "<unknown>"
        lines.append(f"- Location: {file_loc} in `{f.function or '<unknown>'}`")
        lines.append("")
        # primary analysis
        primary: Optional["RuleResult"] = analysis.rule_results[0] if analysis.rule_results else None
        if primary:
            lines.append("## Root Cause")
            lines.append("")
            lines.append(primary.root_cause)
            lines.append("")
            lines.append("## Suggested Fix")
            lines.append("")
            lines.append(primary.suggestion)
            lines.append("")
            lines.append(f"**Confidence:** {primary.confidence:.2f}")
            lines.append("")

        if analysis.rule_results:
            lines.append("## All Rules")
            lines.append("")
            for r in analysis.rule_results:
                lines.append(f"- **{r.rule}** (confidence: {r.confidence:.2f}) — {r.root_cause}")

        return "\n".join(lines)

    def generate_and_save(self, run_result: "RunResult", analysis: AnalysisResult) -> Path:
        content = self.generate(run_result, analysis)
        self.out_path.write_text(content, encoding="utf-8")
        return self.out_path
