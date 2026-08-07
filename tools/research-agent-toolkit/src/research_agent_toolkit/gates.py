from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateDecision:
    status: str
    action: str
    reason: str


def classify(action: str, verify_actions: list[str], deny_actions: list[str]) -> GateDecision:
    if action in deny_actions:
        return GateDecision("DENY", action, "action denied by policy")
    if action in verify_actions:
        return GateDecision("VERIFY", action, "action requires verifier before preservation")
    return GateDecision("ALLOW", action, "action allowed without structural verification gate")
