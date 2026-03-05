from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, List, Optional

from .models import FailureInfo


@dataclass
class RuleResult:
    rule: str
    root_cause: str
    suggestion: str
    confidence: float


class Rule(ABC):
    name: str

    @abstractmethod
    def match(self, failure: FailureInfo) -> bool:
        raise NotImplementedError

    @abstractmethod
    def analyze(self, failure: FailureInfo) -> RuleResult:
        raise NotImplementedError


class TypeErrorMissingArgRule(Rule):
    name = "TypeErrorMissingArg"
    RE = re.compile(r"missing .*required positional argument")

    def match(self, failure: FailureInfo) -> bool:
        if failure.exc_type == "TypeError" and failure.message:
            return bool(self.RE.search(failure.message.lower()))
        return False

    def analyze(self, failure: FailureInfo) -> RuleResult:
        root = "A required positional argument is missing when calling a function."
        suggestion = (
            "Check the function call at the indicated location and provide the missing argument(s); "
            "ensure positional/keyword ordering is correct or provide defaults."
        )
        return RuleResult(self.name, root, suggestion, 0.9)


class ImportErrorRule(Rule):
    name = "ImportError"

    def match(self, failure: FailureInfo) -> bool:
        return failure.exc_type == "ImportError" or (
            failure.message and "cannot import name" in failure.message.lower()
        )

    def analyze(self, failure: FailureInfo) -> RuleResult:
        root = "An import failed, likely due to a missing symbol or circular import."
        suggestion = (
            "Verify the imported symbol exists in the target module, check for circular imports, "
            "and ensure package/module paths are correct."
        )
        return RuleResult(self.name, root, suggestion, 0.8)


class ModuleNotFoundRule(Rule):
    name = "ModuleNotFoundError"

    def match(self, failure: FailureInfo) -> bool:
        if failure.exc_type == "ModuleNotFoundError":
            return True
        if failure.message:
            return bool(re.search(r"no module named ['\"]?([\w\.\-]+)['\"]?", failure.message, re.I))
        return False

    def analyze(self, failure: FailureInfo) -> RuleResult:
        m = re.search(r"no module named ['\"]?([\w\.\-]+)['\"]?", failure.message or "", re.I)
        mod = m.group(1) if m else None
        root = f"A required module is missing: {mod or '<unknown module>'}."
        suggestion = (
            "Install the missing package, or fix PYTHONPATH/virtualenv. If it's a local module, "
            "ensure the import path is correct."
        )
        return RuleResult(self.name, root, suggestion, 0.95 if mod else 0.6)


class AssertionErrorRule(Rule):
    name = "AssertionError"

    def match(self, failure: FailureInfo) -> bool:
        return failure.exc_type == "AssertionError"

    def analyze(self, failure: FailureInfo) -> RuleResult:
        root = "An assertion failed indicating a violated assumption in the code."
        suggestion = (
            "Inspect the assertion and surrounding code; print or log the involved values to see "
            "which assumption was violated and adjust logic or inputs accordingly."
        )
        return RuleResult(self.name, root, suggestion, 0.7)


class AttributeErrorRule(Rule):
    name = "AttributeError"
    RE_NONE = re.compile(r"'none' object has no attribute '(?P<attr>[^']+)'", re.I)
    RE_NO_ATTR = re.compile(r"has no attribute '(?P<attr>[^']+)'", re.I)

    def match(self, failure: FailureInfo) -> bool:
        return failure.exc_type == "AttributeError" or (
            failure.message and "has no attribute" in failure.message.lower()
        )

    def analyze(self, failure: FailureInfo) -> RuleResult:
        msg = failure.message or ""
        if self.RE_NONE.search(msg):
            root = "Attempted to access an attribute on `None`, indicating a None value where an object was expected."
            suggestion = (
                "Trace the variable to see why it's None before the access. Add checks or ensure the variable is initialized."
            )
            confidence = 0.95
        else:
            root = "An attribute was missing on an object or module."
            suggestion = (
                "Check the object's type and initialization. If the attribute is from a library API, confirm the correct version."
            )
            confidence = 0.75
        return RuleResult(self.name, root, suggestion, confidence)


class RuleBasedFailureAnalyzer:
    """Analyze failures using a registry of simple rules.

    The analyzer is extensible: new rules can be registered via `add_rule`.
    """

    def __init__(self, rules: Optional[Iterable[Rule]] = None) -> None:
        self._rules: List[Rule] = []
        if rules:
            for r in rules:
                self.add_rule(r)
        else:
            # register defaults
            self.add_rule(TypeErrorMissingArgRule())
            self.add_rule(ModuleNotFoundRule())
            self.add_rule(ImportErrorRule())
            self.add_rule(AssertionErrorRule())
            self.add_rule(AttributeErrorRule())

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def analyze(self, failure: FailureInfo) -> List[RuleResult]:
        """Return a list of matching RuleResult ordered by confidence (desc).

        If no rules match, a low-confidence generic result is returned.
        """
        results: List[RuleResult] = []
        for r in self._rules:
            try:
                if r.match(failure):
                    results.append(r.analyze(failure))
            except Exception:
                # Don't allow rule failures to break overall analysis
                continue

        if not results:
            results.append(
                RuleResult(
                    rule="Generic",
                    root_cause="Unable to determine root cause from rules.",
                    suggestion=(
                        "Inspect the full traceback and context; consider adding a custom rule for this pattern."
                    ),
                    confidence=0.1,
                )
            )

        return sorted(results, key=lambda r: r.confidence, reverse=True)
