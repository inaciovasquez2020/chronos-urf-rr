#!/usr/bin/env python3
"""Exact exterior rank-loss obstruction for the corrected GfE GQQ block.

In the physical accumulation sector M=1, beta=5/2, lambda=6, omega=i/4,
the corrected block determinant numerator has a real zero strictly outside
the horizon.  This is an obstruction to a global inverse/uniform inverse bound
for GQQ on the full exterior; it is not a claim that the full resolvent or
Riesz projector fails to exist.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_pq_gqq.json"


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    M, beta, lam, omega, r = sp.symbols("M beta lam omega r")
    locals_ = {
        "M": M, "beta": beta, "lam": lam, "lambda": lam,
        "omega": omega, "r": r, "I": sp.I,
    }
    gqq = data["GQQ"]
    if gqq.get("rank_classification") != (
        "rank 2 when Delta != 0; rank 1 when Delta = 0, throughout the ordinary-generator guard"
    ):
        raise AssertionError("corrected GQQ rank classification changed")

    delta = sp.sympify(gqq["determinant_numerator_Delta"], locals=locals_)
    sector = {M: sp.Integer(1), beta: sp.Rational(5, 2), lam: sp.Integer(6), omega: sp.I / 4}
    delta_sector = simp(delta.subs(sector))

    x = sp.symbols("x", real=True)
    p = (
        x**9 + 2*x**8 + 4*x**7 + 452*x**6 - 248*x**5 - 112*x**4
        - 5120*x**3 - 1024*x**2 + 22528*x - 73728
    )
    expected = -sp.Rational(25, 16) * (x - 2) * p
    if simp(delta_sector.subs(r, x) - expected) != 0:
        raise AssertionError("dimensionless exceptional-sector Delta factorization changed")

    left = sp.Rational(257, 100)
    right = sp.Rational(129, 50)
    p_left = sp.factor(p.subs(x, left))
    p_right = sp.factor(p.subs(x, right))
    if not (p_left < 0 and p_right > 0):
        raise AssertionError("exact rational endpoint signs no longer bracket an exterior Delta zero")
    if not (left > 2 and right > left):
        raise AssertionError("rank-loss bracket is not strictly exterior")

    # Every denominator factor of det(GQQ) is nonzero throughout this interval:
    # r>2, -16 M beta + 5 r^3 = 5(r^3-8)>0, and 8 M beta + 5 r^3>0.
    denominator = sp.sympify(gqq["determinant_denominator"], locals=locals_).subs(sector)
    expected_denominator = r**2 * (r - 2)**2 * 5*(r**3 - 8) * (20 + 5*r**3)
    if simp(denominator - expected_denominator) != 0:
        raise AssertionError("GQQ determinant denominator specialization changed")
    for endpoint in (left, right):
        if denominator.subs(r, endpoint) <= 0:
            raise AssertionError("GQQ determinant denominator is not positive at bracket endpoint")

    # The existing exterior-continuation gate certifies det(E) != 0 and
    # coefficient regularity for every r>2 in this same fixed sector.  Thus
    # the bracketed zero lies inside the ordinary-generator guard.
    print("GFE_CORRECTED_GQQ_EXTERIOR_RANKLOSS_OBSTRUCTION_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; lambda=6; omega=I/4")
    print("DIMENSIONLESS_VARIABLE := x=r/M")
    print("DELTA_FACTOR := -25*(x-2)*p(x)/16")
    print(f"P_LEFT := p(257/100) = {p_left}")
    print(f"P_RIGHT := p(129/50) = {p_right}")
    print("EXTERIOR_DELTA_ZERO_EXISTS := x_* in (257/100, 129/50) = (2.57, 2.58)")
    print("GQQ_DETERMINANT_DENOMINATOR := positive throughout the bracket")
    print("ORDINARY_GENERATOR_GUARD := supplied by the exterior-continuation certificate on every r>2")
    print("GQQ_RANK_AT_DELTA_ZERO := 1")
    print("CONSEQUENCE := no global inverse or uniform inverse bound for GQQ over the full exterior")
    print("BOUNDARY := does not by itself disprove full resolvent/Riesz-projector existence or local-uniform convergence")


if __name__ == "__main__":
    main()
