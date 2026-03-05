from __future__ import annotations

from typing import Dict

from .models import FileAnalysis


def summarize(analysis: FileAnalysis) -> Dict[str, int]:
    """Return a small metrics summary for a single FileAnalysis."""
    return {
        "functions": len(analysis.functions),
        "classes": len(analysis.classes),
        "todos": analysis.todo_count,
    }
