#!/usr/bin/env python3
"""Exact full-pencil exclusion test for the exterior |z|=2 contour.

A contour zero at x_* would force the resultant R(z)=Res_x(p(x), det(zE-A))
to vanish at a point z on |z|=2. On that circle, conjugation gives the
reciprocal-conjugate polynomial S(z)=sum_k conjugate(a_k)*4^k*z^(n-k)
for R(z)=sum_k a_k*z^k. Thus gcd(R,S)=1 is an exact certificate that
the contour has no zero for any root of p, including the isolated exterior
root x_* in (2.571,2.572). This stronger all-roots exclusion avoids
numerically substituting an approximation for x_*.
"""
from __future__ import annotations

import json
from pathlib import Path
import hashlib
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    M, beta, lam, omega, r, z, x = sp.symbols("M beta lam omega r z x")
    loc = {"M": M, "beta": beta, "lam": lam, "lambda": lam,
           "omega": omega, "r": r, "I": sp.I}
    substitutions = {M: sp.Integer(1), beta: sp.Rational(5, 2),
                     lam: sp.Integer(6), omega: sp.I / 4, r: x}
    E = sp.Matrix([[sp.sympify(v, locals=loc).subs(substitutions)
                    for v in row] for row in data["descriptor_E"]])
    A = sp.Matrix([[sp.sympify(v, locals=loc).subs(substitutions)
                    for v in row] for row in data["descriptor_A"]])
    pencil = z * E - A
    determinant = sp.cancel(pencil.det(method="domain-ge"))
    numerator, denominator = sp.fraction(determinant)
    numerator = sp.factor(numerator)
    if numerator == 0:
        raise AssertionError("full pencil determinant numerator vanished identically")
    if sp.denom(denominator) != 1:
        raise AssertionError("unexpected nested denominator in determinant denominator")

    p = (x**9 + 2*x**8 + 4*x**7 + 452*x**6 - 248*x**5 - 112*x**4
         - 5120*x**3 - 1024*x**2 + 22528*x - 73728)
    left, right = sp.Rational(2571, 1000), sp.Rational(2572, 1000)
    if sp.Poly(p, x, domain="QQ").count_roots(left, right) != 1:
        raise AssertionError("the exterior algebraic point is not uniquely isolated")

    # Eliminate x. Any zero of the full pencil at any root of p must be a
    # zero of this resultant. The determinant denominator depends only on x,
    # so it cannot create a spurious z-contour zero.
    resultant = sp.factor(sp.resultant(p, numerator, x))
    if resultant == 0:
        raise AssertionError("elimination resultant is identically zero")
    R = sp.Poly(resultant, z, extension=sp.I)
    degree = R.degree()
    if degree < 1:
        raise AssertionError("unexpected constant elimination resultant")

    reciprocal_conjugate = sp.Integer(0)
    for k in range(degree + 1):
        coefficient = sp.conjugate(R.nth(k))
        reciprocal_conjugate += coefficient * 4**k * z**(degree-k)
    S = sp.Poly(sp.expand(reciprocal_conjugate), z, extension=sp.I)
    common = sp.gcd(R, S)
    if common.degree() != 0:
        # This is deliberately a hard failure: a nontrivial gcd needs an
        # additional exact real-algebraic isolation, not a numerical claim.
        raise AssertionError(
            "resultant and reciprocal-conjugate share factors; exact contour "
            "separation is not certified by this test"
        )

    print("GFE_FULL_SIX_STATE_EXTERIOR_CONTOUR_EXCLUSION_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; lambda=6; omega=I/4")
    print("CONTOUR := |z|=2")
    print("EXTERIOR_ROOT := unique root of p(x) in (2571/1000,2572/1000)")
    print(f"DESCRIPTOR_PENCIL_DETERMINANT_NUMERATOR_SHA256 := {hashlib.sha256(str(numerator).encode()).hexdigest()}")
    print(f"ELIMINATION_RESULTANT_DEGREE := {degree}")
    print(f"RECIPROCAL_CONJUGATE_GCD_DEGREE := {common.degree()}")
    print("FULL_PENCIL_NONZERO_ON_CONTOUR := true")
    print("SCOPE := excludes contour intersection at x_*; does not prove global parameter uniformity or all-contour closure")


if __name__ == "__main__":
    main()
