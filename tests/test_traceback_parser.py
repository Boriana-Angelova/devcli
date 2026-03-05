import textwrap
from pathlib import Path

import pytest

from devcli.traceback_parser import TracebackParser


def test_type_error_parsing():
    tb = textwrap.dedent(
        """
        Traceback (most recent call last):
          File "script.py", line 10, in <module>
            foo()
          File "script.py", line 7, in foo
            bar(1)
          File "script.py", line 3, in bar
            raise TypeError("bar() missing 1 required positional argument: 'y'")
        TypeError: bar() missing 1 required positional argument: 'y'
        """
    )

    info = TracebackParser.parse(tb)
    assert info.exc_type == "TypeError"
    assert "missing 1 required positional argument" in info.message
    assert info.file is not None and Path(str(info.file)).name == "script.py"
    assert info.line == 3
    assert info.function == "bar"


def test_import_error_parsing():
    tb = textwrap.dedent(
        """
        Traceback (most recent call last):
          File "script.py", line 2, in <module>
            from package.module import something
        ImportError: cannot import name 'something' from 'package.module' (/path/to/package/module.py)
        """
    )

    info = TracebackParser.parse(tb)
    assert info.exc_type == "ImportError"
    assert "cannot import name 'something'" in info.message
    assert info.file is not None and Path(str(info.file)).name == "script.py"
    assert info.line == 2
    assert info.function == "<module>"


def test_assertion_error_parsing():
    tb = textwrap.dedent(
        """
        Traceback (most recent call last):
          File "test.py", line 5, in check
            assert x > 0, "x must be positive"
        AssertionError: x must be positive
        """
    )

    info = TracebackParser.parse(tb)
    assert info.exc_type == "AssertionError"
    assert "x must be positive" in info.message
    assert info.file is not None and Path(str(info.file)).name == "test.py"
    assert info.line == 5
    assert info.function == "check"
