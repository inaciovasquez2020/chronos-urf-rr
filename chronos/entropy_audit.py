#!/usr/bin/env python3
"""
Chronos witness scaffold.

Goal interface:
  - compute a certified lower bound on ED(F_n) by auditing cumulative information gain
    (currently a placeholder estimator + unit tests).
Replace `per_step_info_bound_bits` and `required_entropy_bits` with the certified values
for your concrete hard family.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class AuditParams:
    n: int
    per_step_info_bound_bits: float  # upper bound on I(X;Y_t|history) per step
    required_entropy_bits: float     # lower bound on H(X)

def lower_bound_steps(params: AuditParams) -> int:
    if params.per_step_info_bound_bits <= 0:
        raise ValueError("per_step_info_bound_bits must be > 0")
    if params.required_entropy_bits < 0:
        raise ValueError("required_entropy_bits must be >= 0")
    # ceil(required / per_step)
    return int((params.required_entropy_bits + params.per_step_info_bound_bits - 1e-12) // params.per_step_info_bound_bits + 1)

def main() -> None:
    # Demo defaults: replace with certified constants for your family
    p = AuditParams(n=1000, per_step_info_bound_bits=4.0, required_entropy_bits=1000.0)
    lb = lower_bound_steps(p)
    print(f"Lower bound steps: {lb}")

if __name__ == "__main__":
    main()
