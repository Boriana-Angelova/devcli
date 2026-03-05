import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class FailureInfo:
    exc_type: str
    message: str
    file: Optional[str]
    line: Optional[int]
    function: str


class TracebackParser:
    @staticmethod
    def parse(traceback_text: str) -> FailureInfo:
        lines = traceback_text.strip().splitlines()

        # Find exception line (last non-empty line)
        exception_line = None
        for line in reversed(lines):
            line = line.strip()
            if line and not line.startswith("Traceback"):
                exception_line = line
                break

        if not exception_line:
            raise ValueError("Invalid traceback format")

        # Extract exception type and message
        match = re.match(r"^(\w+):\s*(.*)", exception_line)
        if not match:
            raise ValueError("Could not parse exception line")

        exc_type = match.group(1)
        message = match.group(2)

        # Extract last stack frame
        file = None
        line_no = None
        function = None

        # Look for last "File ..." line
        for i in range(len(lines) - 1):
            if lines[i].strip().startswith('File "'):
                frame_line = lines[i].strip()

                frame_match = re.match(
                    r'File "(.+)", line (\d+), in (.+)',
                    frame_line,
                )

                if frame_match:
                    file = frame_match.group(1)
                    line_no = int(frame_match.group(2))
                    function = frame_match.group(3)

        return FailureInfo(
            exc_type=exc_type,
            message=message,
            file=file,
            line=line_no,
            function=function if function else "<unknown>",
        )