from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyViolation:
    pattern: str
    line: int
    excerpt: str


def scan_text(text: str, forbidden_patterns: list[str]) -> list[PolicyViolation]:
    violations: list[PolicyViolation] = []
    lines = text.splitlines()
    for pattern in forbidden_patterns:
        rx = re.compile(pattern)
        for idx, line in enumerate(lines, 1):
            if rx.search(line):
                violations.append(PolicyViolation(pattern, idx, line.strip()[:200]))
    return violations
