#!/usr/bin/env python3
"""Certify the one-sided logarithmic Borel boundary asymptotic.

Dependency: the immediately preceding invariant-cone verifier certifies

  K(z) = P_60(z) - A_phys*Li_2(-(18/5)z) + R(z),
  A_phys > 0,

with P_60 polynomial and R in C^1 on the closed disk |z| <= 5/18.
This verifier isolates the exact singular coefficient at the physical boundary
z0=-5/18.  No analytic continuation across the boundary is assumed or claimed.
"""
from __future__ import annotations

import sympy as sp


def main() -> None:
    r = sp.Rational(18, 5)
    radius = sp.Rational(5, 18)
    z0 = -radius
    Aphys = sp.symbols("A_phys", positive=True)
    t = sp.symbols("t", positive=True)
    z = sp.symbols("z")

    if sp.cancel(r * radius - 1) != 0:
        raise AssertionError("Borel radius is not reciprocal to the factorial base")
    if sp.cancel(1 + r * z0) != 0:
        raise AssertionError("physical boundary does not map to the dilogarithmic endpoint")

    # Leading singular model from the certified decomposition.
    lead = -Aphys * sp.polylog(2, -r * z)
    lead_derivative = sp.expand_func(sp.diff(lead, z))
    expected_derivative = Aphys * sp.log(1 + r * z) / z
    if sp.simplify(lead_derivative - expected_derivative) != 0:
        raise AssertionError("dilogarithmic derivative identity changed")

    # Approach the physical boundary from inside the real Borel disk:
    #   z=z0+t, t>0, t->0+.
    boundary_derivative = sp.simplify(expected_derivative.subs(z, z0 + t))
    expected_boundary_derivative = -Aphys * r * sp.log(r * t) / (1 - r * t)
    if sp.simplify(boundary_derivative - expected_boundary_derivative) != 0:
        raise AssertionError("boundary derivative reduction changed")

    # Exact factorization after division by log(t):
    #   lead'(z0+t)/log(t)
    #     = -A_phys*r/(1-r*t) * (1 + log(r)/log(t)).
    derivative_over_log = sp.expand_log(boundary_derivative, force=True) / sp.log(t)
    factorized_derivative_over_log = (
        -Aphys * r / (1 - r * t) * (1 + sp.log(r) / sp.log(t))
    )
    if sp.simplify(derivative_over_log - factorized_derivative_over_log) != 0:
        raise AssertionError("boundary logarithmic derivative factorization changed")

    # The elementary one-sided factors have exact limits 1 and 0.
    if sp.limit(1 / (1 - r * t), t, 0, dir="+") != 1:
        raise AssertionError("rational boundary factor limit changed")
    if sp.limit(sp.log(r) / sp.log(t), t, 0, dir="+") != 0:
        raise AssertionError("constant-log over log(t) limit changed")
    if sp.limit(1 / (1 + 1 / sp.log(t)), t, 0, dir="+") != 1:
        raise AssertionError("l'Hopital denominator factor limit changed")

    # For g(t)=t*log(t), g'(t)=log(t)+1.  Therefore the derivative quotient
    # tends to -r*A_phys, and the standard one-sided l'Hopital theorem gives
    # the same limit for the function quotient.  The certified polynomial and
    # C^1 remainder contribute only O(t), hence vanish after division by
    # t*log(t).
    singular_coefficient = sp.simplify(-r * Aphys)
    if singular_coefficient.is_nonzero is not True:
        raise AssertionError("one-sided logarithmic coefficient is not certified nonzero")
    if singular_coefficient.is_negative is not True:
        raise AssertionError("one-sided logarithmic coefficient sign changed")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOUNDARY_ASYMPTOTIC_CERTIFIED")
    print("DEPENDENCY := invariant-cone verifier certifies K=P_60-A_phys*Li_2(-(18/5)z)+R with A_phys>0 and R in C^1 on the closed Borel disk")
    print("PHYSICAL_BOREL_BOUNDARY := z0=-5/18")
    print("ONE_SIDED_VARIABLE := t=z-z0=z+5/18 -> 0+")
    print("DILOG_BOUNDARY_DERIVATIVE := -A_phys*(18/5)*log((18/5)*t)/(1-(18/5)*t)")
    print("DILOG_DERIVATIVE_OVER_LOG_LIMIT := lead'(z0+t)/log(t) -> -(18/5)*A_phys")
    print("ONE_SIDED_LHOPITAL := [lead(z0+t)-lead(z0)]/[t*log(t)] -> -(18/5)*A_phys")
    print("C1_REMAINDER_QUOTIENT := [P_60(z0+t)-P_60(z0)+R(z0+t)-R(z0)]/[t*log(t)] -> 0")
    print("PHYSICAL_BOREL_ONE_SIDED_QUOTIENT_LIMIT := [K(z0+t)-K(z0)]/[t*log(t)] -> -(18/5)*A_phys")
    print("PHYSICAL_BOREL_ONE_SIDED_LOG_COEFFICIENT := -(18/5)*A_phys != 0")
    print("PHYSICAL_BOREL_ONE_SIDED_EXPANSION := K(z0+t)=K(z0)-(18/5)*A_phys*t*log(t)+O(t)")
    print("BOUNDARY := one-sided interior real asymptotic only; no analytic continuation across z=-5/18 and no Laplace summability claim")


if __name__ == "__main__":
    main()
