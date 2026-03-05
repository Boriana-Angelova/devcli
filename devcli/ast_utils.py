from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class FunctionDefInfo:
    name: str
    lineno: int
    params: List[str]
    defaults: int
    vararg: Optional[str]
    kwarg: Optional[str]
    kwonlyargs: List[str]


@dataclass
class CallInfo:
    func_name: Optional[str]
    lineno: int
    pos_args: int
    kw_args: List[str]
    has_starargs: bool
    has_kwargs: bool


@dataclass
class ParamCount:
    positional: int
    required_positional: int
    defaults: int
    vararg: bool
    kwonly: int
    kwarg: bool


def parse_source(path: Path) -> ast.Module:
    """Parse a Python file and return its AST module."""
    with path.open("r", encoding="utf-8") as f:
        source = f.read()
    return ast.parse(source, filename=str(path))


def iter_functions(node: ast.AST) -> Iterable[ast.FunctionDef]:
    for n in ast.walk(node):
        if isinstance(n, ast.FunctionDef):
            yield n


def iter_classes(node: ast.AST) -> Iterable[ast.ClassDef]:
    for n in ast.walk(node):
        if isinstance(n, ast.ClassDef):
            yield n


def _get_name_from_node(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        value = _get_name_from_node(node.value)
        if value:
            return f"{value}.{node.attr}"
        return node.attr
    if isinstance(node, ast.Call):
        return _get_name_from_node(node.func)
    return None


def extract_function_definitions(file_path: Path) -> List[FunctionDefInfo]:
    """Return a list of FunctionDefInfo for all functions in the file."""
    module = parse_source(file_path)
    results: List[FunctionDefInfo] = []
    for fn in iter_functions(module):
        args = fn.args
        param_names = [a.arg for a in args.args]
        defaults = len(args.defaults or [])
        vararg = args.vararg.arg if args.vararg else None
        kwarg = args.kwarg.arg if args.kwarg else None
        kwonly = [a.arg for a in args.kwonlyargs]
        results.append(
            FunctionDefInfo(
                name=fn.name,
                lineno=fn.lineno,
                params=param_names,
                defaults=defaults,
                vararg=vararg,
                kwarg=kwarg,
                kwonlyargs=kwonly,
            )
        )
    return results


def extract_function_calls(file_path: Path) -> List[CallInfo]:
    """Return a list of CallInfo for all function calls in the file."""
    module = parse_source(file_path)
    calls: List[CallInfo] = []

    for node in ast.walk(module):
        if isinstance(node, ast.Call):
            func_name = _get_name_from_node(node.func)
            pos_args = sum(1 for a in node.args if not isinstance(a, ast.Starred))
            has_starargs = any(isinstance(a, ast.Starred) for a in node.args)
            kw_args = [k.arg for k in node.keywords if k.arg is not None]
            has_kwargs = any(k.arg is None for k in node.keywords)
            calls.append(
                CallInfo(
                    func_name=func_name,
                    lineno=getattr(node, "lineno", -1),
                    pos_args=pos_args,
                    kw_args=kw_args,
                    has_starargs=has_starargs,
                    has_kwargs=has_kwargs,
                )
            )
    return calls


def count_function_parameters(function_name: str, module: Optional[ast.AST] = None) -> Optional[ParamCount]:
    """Count parameters for a function name within the provided AST module.

    If `module` is None, returns None.
    """
    if module is None:
        return None

    target_name = function_name.split(".")[-1]
    for fn in iter_functions(module):
        if fn.name == target_name:
            args = fn.args
            positional = len(args.args)
            defaults = len(args.defaults or [])
            required = max(0, positional - defaults)
            # treat common instance methods by dropping 'self'
            if args.args and args.args[0].arg == "self":
                positional -= 1
                required = max(0, required - 1)
            return ParamCount(
                positional=positional,
                required_positional=required,
                defaults=defaults,
                vararg=bool(args.vararg),
                kwonly=len(args.kwonlyargs),
                kwarg=bool(args.kwarg),
            )
    return None


def detect_argument_mismatch(function_name: str, call_node: ast.Call, module: Optional[ast.AST] = None):
    """Detect simple argument mismatches between a call and a function definition.

    Returns a dict with keys: `match` (bool), `reason` (optional str), `suggestion` (optional str), `confidence` (0-1 float).
    """
    if module is None:
        return {"match": False, "reason": "module not provided", "suggestion": None, "confidence": 0.0}

    param_info = count_function_parameters(function_name, module=module)
    if param_info is None:
        return {"match": False, "reason": "function definition not found", "suggestion": None, "confidence": 0.2}

    pos_args = sum(1 for a in call_node.args if not isinstance(a, ast.Starred))
    has_star = any(isinstance(a, ast.Starred) for a in call_node.args)
    kw_names = [k.arg for k in call_node.keywords if k.arg is not None]
    has_kwargs = any(k.arg is None for k in call_node.keywords)

    # compute allowed ranges
    min_pos = param_info.required_positional
    max_pos = param_info.positional if not param_info.vararg else float("inf")

    if pos_args < min_pos:
        reason = f"Missing {min_pos - pos_args} required positional argument(s)."
        suggestion = "Provide the missing positional arguments or use keyword arguments."
        return {"match": False, "reason": reason, "suggestion": suggestion, "confidence": 0.9}

    if pos_args > max_pos and not has_star:
        reason = f"Too many positional arguments: got {pos_args}, expected at most {param_info.positional}."
        suggestion = "Remove extra positional arguments or pass them as keywords if supported."
        return {"match": False, "reason": reason, "suggestion": suggestion, "confidence": 0.9}

    # detect unknown keyword names (best-effort by comparing names)
    # find function definition to retrieve param names
    target_name = function_name.split(".")[-1]
    fn_node = None
    for fn in iter_functions(module):
        if fn.name == target_name:
            fn_node = fn
            break

    if fn_node is not None:
        param_names = [a.arg for a in fn_node.args.args]
        kwonly = [a.arg for a in fn_node.args.kwonlyargs]
        all_names = set(param_names + kwonly)
        unknown_keywords = [k for k in kw_names if k not in all_names]
        if unknown_keywords and not param_info.kwarg:
            reason = f"Unknown keyword argument(s): {unknown_keywords}."
            suggestion = "Check the parameter names for the function or accept **kwargs in the function signature."
            return {"match": False, "reason": reason, "suggestion": suggestion, "confidence": 0.85}

    return {"match": True, "reason": None, "suggestion": None, "confidence": 1.0}
