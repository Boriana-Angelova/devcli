from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .models import FailureInfo


FRAME_RE = re.compile(r'\s*File "(?P<file>.+?)", line (?P<line>\d+), in (?P<func>.+)')
EXC_RE = re.compile(r'^(?P<type>[A-Za-z_][\w\.]*): (?P<message>.+)$')


class TracebackParser:
    """Parse Python traceback text into a structured `FailureInfo` dataclass."""

    @staticmethod
    def parse(text: str) -> FailureInfo:
        lines = text.strip().splitlines()
        exc_type: str = ""
        message: str = ""
        file_path: Optional[Path] = None
        line_no: Optional[int] = None
        func: Optional[str] = None

        exc_index = None
        # Find the exception line (search from the end)
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            m = EXC_RE.match(line)
            if m:
                exc_type = m.group("type")
                message = m.group("message")
                exc_index = i
                break

        # fallback if no explicit exception line
        if exc_index is None and lines:
            last = lines[-1].strip()
            if ": " in last:
                t, _, msg = last.partition(": ")
                exc_type = t
                message = msg
                exc_index = len(lines) - 1

        # Find the last frame before the exception
        if exc_index is not None:
            for j in range(exc_index - 1, -1, -1):
                m = FRAME_RE.search(lines[j])
                if m:
                    try:
                        file_path = Path(m.group("file"))
                    except Exception:
                        file_path = None
                    try:
                        line_no = int(m.group("line"))
                    except Exception:
                        line_no = None
                    func = m.group("func").strip()
                    break

        return FailureInfo(
            exception_type=exc_type,
            message=message,
            file=file_path,
            line=line_no,
            function=func
        )