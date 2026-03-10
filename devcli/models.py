from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class FunctionInfo:
    name: str
    lineno: int


@dataclass
class ClassInfo:
    name: str
    lineno: int


@dataclass
class FileAnalysis:
    path: Path
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    todo_count: int


@dataclass
class RunResult:
    command: str
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float


@dataclass
class FailureInfo:
    exception_type: str
    message: str
    file: Optional[Path] = None
    line: Optional[int] = None
    function: Optional[str] = None


@dataclass
class AnalysisResult:
    failure: FailureInfo
    rule_results: List["RuleResult"]  # rule_results може да е list, ще съдържа анализираните правила