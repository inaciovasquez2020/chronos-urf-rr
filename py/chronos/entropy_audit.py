from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditParams:
    threshold: float
    depth_limit: int


def lower_bound_steps(params: AuditParams, initial_entropy: float) -> int:
    if params.depth_limit < 0:
        raise ValueError("depth_limit must be nonnegative")
    if params.threshold <= 0:
        raise ValueError("threshold must be positive")
    if initial_entropy <= params.threshold:
        return 0

    entropy = float(initial_entropy)
    steps = 0
    while entropy > params.threshold and steps < params.depth_limit:
        entropy *= 0.5
        steps += 1
    return steps
