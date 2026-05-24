#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class SweepResult:
    eps: float
    R: float
    r_min: float
    r_max: float
    samples: int
    n_min: float
    n_max: float
    alpha_min: float
    alpha_max: float
    min_dn_dr: float
    max_dn_dr: float
    min_dalpha_dr: float
    max_dalpha_dr: float
    n_strictly_increases: bool
    alpha_strictly_decreases: bool
    dn_dr_positive: bool
    dalpha_dr_negative: bool
    alpha_bounded_by_4: bool
    passed: bool


def compute_sweep(eps: float, R: float, r_min: float, r_max: float, samples: int) -> SweepResult:
    if not (0.0 < eps < 1.0):
        raise ValueError("expected 0 < eps < 1")
    if not (R > 0.0):
        raise ValueError("expected R > 0")
    if not (r_max > r_min):
        raise ValueError("expected r_max > r_min")
    if samples < 2:
        raise ValueError("expected samples >= 2")

    def n(r: float) -> float:
        return 1.0 - eps * math.exp(-r / R)

    def alpha(r: float) -> float:
        return n(r) ** -2

    def dn_dr(r: float) -> float:
        return (eps / R) * math.exp(-r / R)

    def dalpha_dr(r: float) -> float:
        return -2.0 * (n(r) ** -3) * dn_dr(r)

    rs = [r_min + (r_max - r_min) * i / (samples - 1) for i in range(samples)]
    ns = [n(r) for r in rs]
    alphas = [alpha(r) for r in rs]
    dns = [dn_dr(r) for r in rs]
    dalphas = [dalpha_dr(r) for r in rs]

    n_strictly_increases = all(ns[i] < ns[i + 1] for i in range(samples - 1))
    alpha_strictly_decreases = all(alphas[i] > alphas[i + 1] for i in range(samples - 1))
    dn_dr_positive = all(x > 0.0 for x in dns)
    dalpha_dr_negative = all(x < 0.0 for x in dalphas)
    alpha_bounded_by_4 = max(alphas) <= 4.0

    passed = all([
        n_strictly_increases,
        alpha_strictly_decreases,
        dn_dr_positive,
        dalpha_dr_negative,
        alpha_bounded_by_4,
    ])

    return SweepResult(
        eps=eps,
        R=R,
        r_min=r_min,
        r_max=r_max,
        samples=samples,
        n_min=min(ns),
        n_max=max(ns),
        alpha_min=min(alphas),
        alpha_max=max(alphas),
        min_dn_dr=min(dns),
        max_dn_dr=max(dns),
        min_dalpha_dr=min(dalphas),
        max_dalpha_dr=max(dalphas),
        n_strictly_increases=n_strictly_increases,
        alpha_strictly_decreases=alpha_strictly_decreases,
        dn_dr_positive=dn_dr_positive,
        dalpha_dr_negative=dalpha_dr_negative,
        alpha_bounded_by_4=alpha_bounded_by_4,
        passed=passed,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eps", type=float, default=0.5)
    parser.add_argument("--R", type=float, default=10.0)
    parser.add_argument("--r-min", type=float, default=0.0)
    parser.add_argument("--r-max", type=float, default=100.0)
    parser.add_argument("--samples", type=int, default=10001)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = compute_sweep(args.eps, args.R, args.r_min, args.r_max, args.samples)

    if args.json:
        print(json.dumps(asdict(result), indent=2, sort_keys=True))
    else:
        print("LARGER-SCALE FINITE-CAPACITY OPTICAL METRIC TEST")
        print(f"eps = {result.eps}")
        print(f"R = {result.R}")
        print(f"domain = [{result.r_min}, {result.r_max}]")
        print(f"samples = {result.samples}")
        print(f"n_min = {result.n_min:.12f}")
        print(f"n_max = {result.n_max:.12f}")
        print(f"alpha_min = {result.alpha_min:.12f}")
        print(f"alpha_max = {result.alpha_max:.12f}")
        print(f"min dn/dr = {result.min_dn_dr:.12e}")
        print(f"max dn/dr = {result.max_dn_dr:.12e}")
        print(f"min dalpha/dr = {result.min_dalpha_dr:.12e}")
        print(f"max dalpha/dr = {result.max_dalpha_dr:.12e}")
        print("PASS" if result.passed else "FAIL")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
