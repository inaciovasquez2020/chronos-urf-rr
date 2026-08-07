from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .budgets import Budget
from .gates import classify
from .policy import scan_text
from .scope import check_paths


@dataclass
class EngineDecision:
    status: str
    reasons: list[str]


def load_config(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def evaluate(config: dict, action: str, paths: list[str], candidate_text: str | None = None, budget: Budget | None = None) -> EngineDecision:
    reasons: list[str] = []
    scope = config.get("scope", {})
    decisions = check_paths(paths, scope.get("allow", []), scope.get("deny", []))
    denied = [x for x in decisions if not x.allowed]
    if denied:
        return EngineDecision("DENY", [f"{x.path}: {x.reason}" for x in denied])

    gate = classify(action, config.get("gates", {}).get("verify_actions", []), config.get("gates", {}).get("deny_actions", []))
    if gate.status == "DENY":
        return EngineDecision("DENY", [gate.reason])
    reasons.append(gate.reason)

    if candidate_text is not None:
        violations = scan_text(candidate_text, config.get("policy", {}).get("forbidden_patterns", []))
        if violations:
            first = violations[0]
            return EngineDecision("DENY", [f"forbidden pattern {first.pattern!r} at line {first.line}: {first.excerpt}"])

    if budget is not None and action in {"modify", "delete", "artifact_regeneration", "theorem_claim"}:
        budget.consume("mutations", 1)

    return EngineDecision(gate.status, reasons)
