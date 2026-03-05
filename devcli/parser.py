from __future__ import annotations

from pathlib import Path
from typing import List

from . import ast_utils, models


def parse_file(path: Path) -> models.FileAnalysis:
    """Parse a single Python file into a FileAnalysis model.

    Counting of TODOs is done via a simple textual scan (fast and predictable).
    """
    module = ast_utils.parse_source(path)

    functions: List[models.FunctionInfo] = [
        models.FunctionInfo(n.name, n.lineno) for n in ast_utils.iter_functions(module)
    ]

    classes: List[models.ClassInfo] = [
        models.ClassInfo(n.name, n.lineno) for n in ast_utils.iter_classes(module)
    ]

    with path.open("r", encoding="utf-8") as f:
        text = f.read()
    todo_count = text.count("TODO")

    return models.FileAnalysis(path=path, functions=functions, classes=classes, todo_count=todo_count)
