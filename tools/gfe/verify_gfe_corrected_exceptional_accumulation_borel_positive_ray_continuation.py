#!/usr/bin/env python3
"""Certify the exact positive-ray continuation hypotheses for the physical Borel germ.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

Dependencies already certified earlier in CI:

* the physical order-2 Borel germ (Xi,K) is analytic on |z|<5/18;
* the constrained 44-state first-order system is exact;
* its theta-form coefficients have no finite denominator zero except z=-5/18;
* the ordinary 1/z origin pole is removable on the physical germ.

This verifier selects the exact seed point z*=1/10 inside the certified Borel disk
and audits the ordinary first-order coefficient matrix along the positive real ray.
Every nontrivial denominator factor is among {z,18*z+5}; for t>0 both are
strictly positive.  Thus the coefficient matrix is analytic on every compact
positive interval [z*,T].  By the standard existence/uniqueness theorem for
linear analytic ODE systems, the physical germ therefore admits unique analytic
continuation from z* to every finite point t>0 on the positive ray.  Together
with the already-certified germ on [0,z*], this closes finite positive-ray
continuation.  No growth-at-infinity or Laplace-summability claim is made.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_first_order_system as fo
import verify_gfe_corrected_exceptional_accumulation_borel_origin_removability as origin
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def rational_power_at_infinity(expr: sp.Expr, z: sp.Symbol) -> int:
    expr = rr.simp(expr)
    if rr.is_zero_expr(expr):
        return -10**9
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    return int(sp.Poly(num, z, domain="QQ").degree() - sp.Poly(den, z, domain="QQ").degree())


def main() -> None:
    z, top_u, top_v, constraint = origin.build_top_rules()
    if len(top_u) != 44 or len(top_v) != 44 or len(constraint) != 44:
        raise AssertionError("44-state first-order data changed")

    allowed = [
        sp.Poly(z, z, domain="QQ").monic(),
        sp.Poly(18 * z + 5, z, domain="QQ").monic(),
    ]

    theta_lcm, theta_nonconstant, theta_origin_order = fo.denominator_lcm(
        top_u + top_v, z, allowed
    )
    expected_theta_lcm = sp.Poly(18 * z + 5, z, domain="QQ").monic().as_expr()
    if sp.Poly(theta_lcm, z, domain="QQ").monic() != sp.Poly(expected_theta_lcm, z, domain="QQ").monic():
        raise AssertionError(f"theta denominator changed: {sp.sstr(theta_lcm)}")
    if theta_origin_order != 0:
        raise AssertionError("theta-system reacquired an origin pole")

    ordinary_exprs = [sp.Integer(1) / z]
    ordinary_exprs += [rr.simp(value / z) for value in top_u + top_v]
    ordinary_lcm, ordinary_nonconstant, ordinary_origin_order = fo.denominator_lcm(
        ordinary_exprs, z, allowed
    )
    expected_ordinary_lcm = sp.Poly(z * (18 * z + 5), z, domain="QQ").monic().as_expr()
    if sp.Poly(ordinary_lcm, z, domain="QQ").monic() != sp.Poly(expected_ordinary_lcm, z, domain="QQ").monic():
        raise AssertionError(f"ordinary denominator changed: {sp.sstr(ordinary_lcm)}")
    if ordinary_origin_order != 1:
        raise AssertionError("ordinary-system origin pole order changed")

    # Exact bridge point inside the certified local Borel disk.
    seed = sp.Rational(1, 10)
    radius = sp.Rational(5, 18)
    pole = -radius
    if not (sp.Rational(0) < seed < radius):
        raise AssertionError("positive-ray seed left the certified local Borel disk")
    if not pole < 0:
        raise AssertionError("physical Borel pole is no longer on the negative real axis")

    # Exact positive-ray denominator audit.  For t>0, t>0 and 18*t+5>5>0.
    t = sp.symbols("t", positive=True)
    if sp.expand((18 * t + 5) - (5 + 18 * t)) != 0:
        raise AssertionError("positive-ray nonzero denominator identity changed")
    if sp.solve(sp.Eq(18 * t + 5, 0), t) != []:
        # SymPy may retain assumptions inconsistently across versions, so use the exact root check below.
        roots = sp.solve(sp.Eq(18 * sp.symbols("s") + 5, 0), sp.symbols("s"))
        if roots != [sp.Rational(-5, 18)]:
            raise AssertionError("linear denominator root changed")
    if sp.Rational(-5, 18) >= 0:
        raise AssertionError("nonzero Borel pole entered the positive ray")

    # A quantitative right-half-plane separation that also covers the ray:
    # |18 z+5|^2=(18 x+5)^2+(18 y)^2 >= 25 whenever x>=0.
    x, y = sp.symbols("x y", nonnegative=True, real=True)
    modulus_sq_minus_25 = sp.expand((18 * x + 5) ** 2 + (18 * y) ** 2 - 25)
    expected_nonnegative_form = sp.expand(324 * x**2 + 180 * x + 324 * y**2)
    if sp.expand(modulus_sq_minus_25 - expected_nonnegative_form) != 0:
        raise AssertionError("right-half-plane pole-separation identity changed")

    # Diagnostic for the next bounded task: exact rational power growth of the
    # ordinary solved top rows.  This is not yet a solution-growth estimate.
    ordinary_top = [rr.simp(value / z) for value in top_u + top_v]
    powers = [rational_power_at_infinity(value, z) for value in ordinary_top if not rr.is_zero_expr(value)]
    if not powers:
        raise AssertionError("ordinary solved top rows vanished")
    max_power = max(powers)
    min_power = min(powers)

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_POSITIVE_RAY_CONTINUATION_CERTIFIED")
    print("DEPENDENCY := local physical Borel germ analytic on |z|<5/18; constrained first-order system and origin removability already certified")
    print("LOCAL_GERM_RADIUS := 5/18")
    print("POSITIVE_RAY_SEED := 1/10")
    print("SEED_INSIDE_LOCAL_GERM := 0 < 1/10 < 5/18")
    print(f"THETA_SYSTEM_DENOMINATOR_LCM := {sp.sstr(theta_lcm)}")
    print(f"THETA_SYSTEM_NONCONSTANT_DENOMINATOR_COUNT := {theta_nonconstant}")
    print("THETA_SYSTEM_ORIGIN_POLE_ORDER := 0")
    print(f"ORDINARY_SYSTEM_DENOMINATOR_LCM := {sp.sstr(ordinary_lcm)}")
    print(f"ORDINARY_SYSTEM_NONCONSTANT_DENOMINATOR_COUNT := {ordinary_nonconstant}")
    print("ORDINARY_SYSTEM_ORIGIN_POLE_ORDER := 1")
    print("POSITIVE_RAY_DENOMINATOR_FACTORS := t and 18*t+5")
    print("POSITIVE_RAY_POLE_FREE := certified for every real t>0")
    print("RIGHT_HALF_PLANE_SEPARATION := |18*z+5|^2 >= 25 for Re(z)>=0")
    print("FINITE_POSITIVE_INTERVAL_COEFFICIENT_ANALYTICITY := certified for every [1/10,T], T>=1/10")
    print("STANDARD_LINEAR_ODE_CONTINUATION := unique analytic continuation from z=1/10 to every finite t>0 on the positive ray")
    print("PHYSICAL_POSITIVE_RAY_CONTINUATION := closed to every finite t>=0 by local germ plus standard linear ODE continuation")
    print(f"ORDINARY_TOP_ROW_RATIONAL_POWER_AT_INFINITY_RANGE := [{min_power},{max_power}]")
    print("INFINITY_GROWTH_STATUS := coefficient growth exposed only; no solution-growth bound")
    print("BOUNDARY := finite positive-ray analytic continuation certified; no bound at t=infinity, no order-2 Laplace convergence, no horizon-to-r_c map, no C_phys, no global Chronos closure")


if __name__ == "__main__":
    main()
