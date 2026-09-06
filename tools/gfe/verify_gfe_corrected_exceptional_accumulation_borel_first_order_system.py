#!/usr/bin/env python3
"""Certify an exact constrained first-order system for the reduced Borel rows.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The preceding certificates construct two polynomial Ore rows R0,R1 in
Q[z]<theta>, theta=z d/dz, with row orders [22,21] and row-leading determinant

  Delta(z) = 625*z*(18*z+5)/64.

A naive differentiation of R1 would weaken R1=0 to theta R1=0.  Instead this
verifier keeps R1=0 as an explicit invariant constraint and uses the pair

  R0 = 0,   theta R1 = 0

to solve exactly for (theta^22 Xi, theta^22 K).  The 44-component jet state

  Y=(Xi,...,theta^21 Xi,K,...,theta^21 K)^T

then obeys a first-order theta-system theta Y=A_theta(z)Y together with the
constraint C(z)Y=0.  The verifier proves coefficient-by-coefficient that:

* the solved top-jet rules make R0 and theta R1 vanish identically;
* theta(CY)=0 under the first-order system, so C Y=0 is preserved;
* every rational coefficient of the theta- and ordinary-derivative systems has
  finite denominator support contained in {z,18*z+5}.

This is an exact algebraic/meromorphic system certificate.  It does not yet
classify z=0 as removable, nor prove analytic continuation or summability.
"""
from __future__ import annotations

import sympy as sp
import verify_gfe_corrected_exceptional_accumulation_borel_reduced_denominators as rd
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def coeffs_through(expr: sp.Expr, theta: sp.Symbol, order: int) -> list[sp.Expr]:
    if rr.is_zero_expr(expr):
        return [sp.Integer(0)] * (order + 1)
    poly = sp.Poly(sp.expand(expr), theta, domain="EX")
    return [rr.simp(poly.coeff_monomial(theta**k)) for k in range(order + 1)]


def denominator_lcm(
    exprs: list[sp.Expr], z: sp.Symbol, allowed: list[sp.Poly]
) -> tuple[sp.Expr, int, int]:
    lcm_poly = sp.Poly(1, z, domain="QQ")
    nonconstant = 0
    max_origin_order = 0
    z_monic = sp.Poly(z, z, domain="QQ").monic()

    for expr in exprs:
        if rr.is_zero_expr(expr):
            continue
        _, den = sp.fraction(sp.cancel(sp.together(expr)))
        den_poly = sp.Poly(den, z, domain="QQ")
        if den_poly.degree() <= 0:
            continue
        nonconstant += 1
        _, factors = sp.factor_list(den_poly.as_expr(), z)
        for factor, exponent in factors:
            factor_poly = sp.Poly(factor, z, domain="QQ").monic()
            if not any(factor_poly == candidate for candidate in allowed):
                raise AssertionError(
                    "unexpected first-order denominator factor: " + sp.sstr(factor)
                )
            if factor_poly == z_monic:
                max_origin_order = max(max_origin_order, int(exponent))
        lcm_poly = sp.lcm(lcm_poly, den_poly.monic())

    return sp.factor(lcm_poly.as_expr()), nonconstant, max_origin_order


def main() -> None:
    rows, z, theta, steps = rd.reconstruct_reduced_rows()
    orders = [rr.row_order(row, theta) for row in rows]
    if orders != [22, 21]:
        raise AssertionError(f"reduced row orders changed: {orders}")

    row0, row1 = rows
    drow1 = rr.theta_left_row(row1, z, theta, 1)
    if rr.row_order(drow1, theta) != 22:
        raise AssertionError("theta R1 did not have order 22")

    lead0 = rr.leading_vector(row0, theta)
    lead1 = rr.leading_vector(row1, theta)
    a, b = lead0
    c, d = lead1
    det = rr.simp(a * d - b * c)
    expected_det = sp.Rational(625, 64) * z * (18 * z + 5)
    if not rr.is_zero_expr(det - expected_det):
        raise AssertionError(f"top-jet determinant changed: {sp.sstr(det)}")

    # Jet state: u_k=theta^k Xi, v_k=theta^k K for 0<=k<=21.
    jet_order = 21
    dim = 2 * (jet_order + 1)

    r0u = coeffs_through(row0[0], theta, 22)
    r0v = coeffs_through(row0[1], theta, 22)
    dr1u = coeffs_through(drow1[0], theta, 22)
    dr1v = coeffs_through(drow1[1], theta, 22)
    r1u = coeffs_through(row1[0], theta, 21)
    r1v = coeffs_through(row1[1], theta, 21)

    lower0 = [r0u[k] for k in range(22)] + [r0v[k] for k in range(22)]
    lower1 = [dr1u[k] for k in range(22)] + [dr1v[k] for k in range(22)]

    # Solve [[a,b],[c,d]] [u_22,v_22]^T = -[lower0,lower1]^T.
    top_u: list[sp.Expr] = []
    top_v: list[sp.Expr] = []
    for j in range(dim):
        top_u.append(rr.simp(-(d * lower0[j] - b * lower1[j]) / det))
        top_v.append(rr.simp((c * lower0[j] - a * lower1[j]) / det))

    # Exact residual check, coefficient-by-coefficient in the 44 jet variables.
    for j in range(dim):
        if not rr.is_zero_expr(a * top_u[j] + b * top_v[j] + lower0[j]):
            raise AssertionError(f"R0 top-jet solve failed at state column {j}")
        if not rr.is_zero_expr(c * top_u[j] + d * top_v[j] + lower1[j]):
            raise AssertionError(f"theta R1 top-jet solve failed at state column {j}")

    # Constraint C(z)Y=R1=0 on the 44-jet state.
    constraint = [r1u[k] for k in range(22)] + [r1v[k] for k in range(22)]
    if all(rr.is_zero_expr(value) for value in constraint):
        raise AssertionError("R1 constraint vanished identically")

    # Prove theta(CY)=0 under the system.  For k<21, theta u_k=u_(k+1)
    # and theta v_k=v_(k+1); for k=21 use the solved top-jet rules.
    propagated = [rr.simp(z * sp.diff(constraint[j], z)) for j in range(dim)]
    for k in range(21):
        propagated[k + 1] = rr.simp(propagated[k + 1] + constraint[k])
        vk = 22 + k
        propagated[vk + 1] = rr.simp(propagated[vk + 1] + constraint[vk])

    cu_top = constraint[21]
    cv_top = constraint[43]
    for j in range(dim):
        propagated[j] = rr.simp(
            propagated[j] + cu_top * top_u[j] + cv_top * top_v[j]
        )
    bad = [j for j, value in enumerate(propagated) if not rr.is_zero_expr(value)]
    if bad:
        raise AssertionError(f"R1 invariant-constraint propagation failed at columns {bad[:8]}")

    # Complete rational denominator audit.  Chain equations in theta-form are
    # polynomial; only the two solved top rows can introduce denominators.
    allowed = [
        sp.Poly(z, z, domain="QQ").monic(),
        sp.Poly(18 * z + 5, z, domain="QQ").monic(),
    ]
    theta_lcm, theta_nonconstant, theta_origin_order = denominator_lcm(
        top_u + top_v, z, allowed
    )

    # In ordinary derivative form Y'=(A_theta/z)Y, every chain shift is 1/z.
    ordinary_exprs = [sp.Integer(1) / z]
    ordinary_exprs += [rr.simp(value / z) for value in top_u + top_v]
    ordinary_lcm, ordinary_nonconstant, ordinary_origin_order = denominator_lcm(
        ordinary_exprs, z, allowed
    )

    # The known nonzero Borel degeneracy must remain represented in the
    # ordinary first-order denominator; z=0 is tracked separately.
    ordinary_poly = sp.Poly(ordinary_lcm, z, domain="QQ")
    if sp.rem(ordinary_poly, sp.Poly(18 * z + 5, z, domain="QQ")) != 0:
        raise AssertionError("ordinary first-order denominator lost z=-5/18")
    if sp.rem(ordinary_poly, sp.Poly(z, z, domain="QQ")) != 0:
        raise AssertionError("ordinary first-order denominator lost z=0")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_FIRST_ORDER_SYSTEM_CERTIFIED")
    print("STATE := Y=(Xi,theta Xi,...,theta^21 Xi,K,theta K,...,theta^21 K)^T")
    print(f"STATE_DIMENSION := {dim}")
    print("TOP_JET_EQUATIONS := R0=0 and theta(R1)=0")
    print("RETAINED_INVARIANT_CONSTRAINT := R1=0")
    print("TOP_JET_DETERMINANT := 625*z*(18*z+5)/64")
    print("TOP_JET_SOLVE_RESIDUAL := exact zero coefficient-by-coefficient")
    print("INVARIANT_CONSTRAINT_PROPAGATION := theta(R1)=0 identically under the first-order system")
    print(f"THETA_SYSTEM_DENOMINATOR_LCM := {sp.sstr(theta_lcm)}")
    print(f"THETA_SYSTEM_NONCONSTANT_DENOMINATOR_COUNT := {theta_nonconstant}")
    print(f"THETA_SYSTEM_MAX_ORIGIN_POLE_ORDER := {theta_origin_order}")
    print(f"ORDINARY_DERIVATIVE_SYSTEM_DENOMINATOR_LCM := {sp.sstr(ordinary_lcm)}")
    print(f"ORDINARY_SYSTEM_NONCONSTANT_DENOMINATOR_COUNT := {ordinary_nonconstant}")
    print(f"ORDINARY_SYSTEM_MAX_ORIGIN_POLE_ORDER := {ordinary_origin_order}")
    print("FINITE_DENOMINATOR_FACTOR_SUPPORT := {z,18*z+5}")
    print("NONZERO_FINITE_DENOMINATOR_POINT := -5/18")
    print("EQUIVALENCE_DOMAIN := any connected domain avoiding z=0 and z=-5/18, with R1=0 imposed at one point")
    print("BOUNDARY := constrained first-order meromorphic system certified; removability at z=0, genuine-singularity classification beyond the known physical -5/18 endpoint, analytic continuation, and Laplace summability remain unproved")


if __name__ == "__main__":
    main()
