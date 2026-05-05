from dataclasses import dataclass


@dataclass(frozen=True)
class AuditParams:
    threshold: float
    depth_limit: int


def lower_bound_steps(params: AuditParams, initial_entropy: float) -> int:
    if params.depth_limit <= 0:
        return 0
    if initial_entropy >= params.threshold:
        return 0
    return params.depth_limit
