#!/usr/bin/env python3
"""Certify descriptor rank-loss coalescence with the horizon at beta=5 M^2/2.

The corrected principal determinant is read from the authoritative Euler artifact.
In the physical accumulation sector beta=5 M^2/2, lambda=6, its positive
finite-radius factor -16 M beta + 5 r^3 becomes 5(r^3-8 M^3), so the nominal
crossing radius r_c=(16 M beta/5)^(1/3) equals 2M exactly.  The specialized
principal determinant has no zero for r>2M.

This removes the separate horizon-to-r_c crossing problem in this fixed sector;
it does not by itself construct the Borel-Laplace horizon solution.
"""
from __future__ import annotations

import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = sp.symbols("M beta lam omega r")
    locals_ = {"M": M, "beta": beta, "lam": lam, "omega": omega, "r": r, "I": sp.I}
    det = sp.factor(sp.sympify(data["principal_determinant"], locals=locals_))

    expected = sp.factor(
        beta**2 * lam**2 * (lam - 2) * (r - 2*M)**3
        * (-16*M*beta + 5*r**3) * (8*M*beta + 5*r**3)
        / (36*r**11)
    )
    if sp.factor(det - expected) != 0:
        raise AssertionError("authoritative principal determinant changed")

    beta_acc = sp.Rational(5, 2) * M**2
    rc_cubed = sp.factor(16*M*beta_acc/5)
    if sp.factor(rc_cubed - (2*M)**3) != 0:
        raise AssertionError("accumulation rank-loss radius no longer equals horizon cubed")

    det_acc = sp.factor(det.subs({beta: beta_acc, lam: 6}))
    expected_acc = sp.factor(
        625 * M**4 * (r - 2*M)**4
        * (r**2 + 2*M*r + 4*M**2)
        * (r**3 + 4*M**3) / r**11
    )
    if sp.factor(det_acc - expected_acc) != 0:
        raise AssertionError("accumulation determinant factorization changed")

    # Exact factor identities behind the extra horizon zero.
    if sp.expand((r**3 - 8*M**3) - (r - 2*M)*(r**2 + 2*M*r + 4*M**2)) != 0:
        raise AssertionError("difference-of-cubes factorization changed")
    if sp.factor((-16*M*beta + 5*r**3).subs(beta, beta_acc) - 5*(r-2*M)*(r**2+2*M*r+4*M**2)) != 0:
        raise AssertionError("rank-loss factor did not coalesce with r-2M")

    # Positivity decomposition on M>0, r>2M.  Put r=2M+x with x>0.
    x = sp.symbols("x", positive=True)
    q2 = sp.expand((r**2 + 2*M*r + 4*M**2).subs(r, 2*M+x))
    q3 = sp.expand((r**3 + 4*M**3).subs(r, 2*M+x))
    if sp.expand(q2 - (12*M**2 + 6*M*x + x**2)) != 0:
        raise AssertionError("positive quadratic factor decomposition changed")
    if sp.expand(q3 - (12*M**3 + 12*M**2*x + 6*M*x**2 + x**3)) != 0:
        raise AssertionError("positive cubic factor decomposition changed")
    # Every displayed coefficient is strictly positive for M>0,x>0.
    q2_poly = sp.Poly(q2, x, M, domain="QQ")
    q3_poly = sp.Poly(q3, x, M, domain="QQ")
    if any(c <= 0 for c in q2_poly.coeffs()) or any(c <= 0 for c in q3_poly.coeffs()):
        raise AssertionError("exterior positivity decomposition lost positive coefficients")

    # Exact horizon multiplicity: specialized numerator contains (r-2M)^4
    # and the remaining factors are nonzero at r=2M for M!=0.
    residual_at_horizon = sp.factor(
        (r**2 + 2*M*r + 4*M**2).subs(r, 2*M)
        * (r**3 + 4*M**3).subs(r, 2*M)
    )
    if sp.factor(residual_at_horizon - 144*M**5) != 0:
        raise AssertionError("horizon residual factor changed")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_RANKLOSS_COALESCENCE_CERTIFIED")
    print("BETA_ACCUMULATION := 5*M^2/2")
    print("NOMINAL_RANKLOSS_RADIUS_CUBED := 8*M^3=(2*M)^3")
    print("RANKLOSS_RADIUS := r_c=2*M for physical M>0")
    print("SPECIALIZED_PRINCIPAL_DETERMINANT := 625*M^4*(r-2*M)^4*(r^2+2*M*r+4*M^2)*(r^3+4*M^3)/r^11")
    print("HORIZON_ZERO_MULTIPLICITY := 4")
    print("EXTERIOR_POSITIVITY := specialized determinant is strictly positive for M>0 and r>2*M")
    print("FINITE_EXTERIOR_RANKLOSS_SET := empty")
    print("HORIZON_TO_RC_INTERVAL := collapses to zero length")
    print("C_PHYS_CROSSING_REQUIREMENT := absent in this fixed accumulation sector; no separate exterior crossing exists")
    print("BOUNDARY := rank-loss coalescence/exterior regularity only; actual Borel-Laplace horizon solution still required")


if __name__ == "__main__":
    main()
