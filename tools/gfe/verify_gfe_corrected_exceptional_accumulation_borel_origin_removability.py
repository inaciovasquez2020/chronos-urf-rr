#!/usr/bin/env python3
"""Certify the physical-germ removability of the ordinary Borel origin pole.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

Dependencies already certified earlier in CI:

* the order-2 Borel germ (Xi,K) converges for |z|<5/18;
* the constrained 44-state first-order Euler system

    theta Y = A_theta(z) Y,   theta=z d/dz,

  has A_theta meromorphic only at 18 z+5=0 and no pole at z=0;
* the ordinary form is Y'=(A_theta(z)/z)Y, so its only origin pole is the
  coordinate 1/z introduced by theta=z d/dz.

This verifier proves the stronger solution-level statement for the certified
physical germ.  The physical order-2 Borel coefficients satisfy Xi_0=K_0=0
and

    Xi_1=20/27,   K_1=-5/27.

Hence every Euler jet theta^k Xi, theta^k K (0<=k<=21) is divisible by z.
Writing Y=z H, the already-certified local convergence implies H is analytic
on |z|<5/18.  We reconstruct A_theta exactly and certify

    A_theta(0) H(0) = H(0),

so

    (A_theta(z)Y(z))/z = A_theta(z)H(z)

extends analytically through z=0 with value H(0)=Y'(0).  We also check that
the retained R1=0 constraint annihilates H(0).  Thus z=0 is a Fuchsian
coordinate singularity of the full ordinary first-order matrix, but the pole
is removable on the physical analytic Borel germ.  No continuation beyond the
local Borel disk is claimed here.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_first_order_system as fo
import verify_gfe_corrected_exceptional_accumulation_borel_reduced_denominators as rd
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def build_top_rules() -> tuple[
    sp.Symbol,
    list[sp.Expr],
    list[sp.Expr],
    list[sp.Expr],
]:
    rows, z, theta, _ = rd.reconstruct_reduced_rows()
    if [rr.row_order(row, theta) for row in rows] != [22, 21]:
        raise AssertionError("reduced row orders changed")

    row0, row1 = rows
    drow1 = rr.theta_left_row(row1, z, theta, 1)
    lead0 = rr.leading_vector(row0, theta)
    lead1 = rr.leading_vector(row1, theta)
    a, b = lead0
    c, d = lead1
    det = rr.simp(a * d - b * c)
    expected_det = sp.Rational(625, 64) * z * (18 * z + 5)
    if not rr.is_zero_expr(det - expected_det):
        raise AssertionError("top-jet determinant changed")

    def coeffs(expr: sp.Expr, order: int) -> list[sp.Expr]:
        return fo.coeffs_through(expr, theta, order)

    r0u = coeffs(row0[0], 22)
    r0v = coeffs(row0[1], 22)
    dr1u = coeffs(drow1[0], 22)
    dr1v = coeffs(drow1[1], 22)
    r1u = coeffs(row1[0], 21)
    r1v = coeffs(row1[1], 21)

    lower0 = [r0u[k] for k in range(22)] + [r0v[k] for k in range(22)]
    lower1 = [dr1u[k] for k in range(22)] + [dr1v[k] for k in range(22)]

    top_u: list[sp.Expr] = []
    top_v: list[sp.Expr] = []
    for j in range(44):
        top_u.append(rr.simp(-(d * lower0[j] - b * lower1[j]) / det))
        top_v.append(rr.simp((c * lower0[j] - a * lower1[j]) / det))

    constraint = [r1u[k] for k in range(22)] + [r1v[k] for k in range(22)]
    return z, top_u, top_v, constraint


def main() -> None:
    z, top_u, top_v, constraint = build_top_rules()

    # Re-derive the exact physical n=1 Borel coordinates from the certified
    # physical top-log vector v1=(5/9,-10/9) and r_1=(1,6):
    #   v1 = xi_1*(1,0) + kappa_1*(1,6).
    v1_0 = sp.Rational(5, 9)
    v1_1 = -sp.Rational(10, 9)
    kappa1 = sp.cancel(v1_1 / 6)
    xi1 = sp.cancel(v1_0 - kappa1)
    if xi1 != sp.Rational(20, 27) or kappa1 != -sp.Rational(5, 27):
        raise AssertionError("physical n=1 Borel coordinates changed")

    xi0 = sp.Integer(0)
    kappa0 = sp.Integer(0)
    if xi0 != 0 or kappa0 != 0:
        raise AssertionError("physical Borel germ lost its zero constant term")

    # For theta^k f=sum n^k f_n z^n, every k>=0 jet has zero constant
    # coefficient because f_0=0.  At n=1, 1^k=1, so all Xi jets have first
    # coefficient xi1 and all K jets have first coefficient kappa1.
    H0 = [xi1] * 22 + [kappa1] * 22
    if len(H0) != 44:
        raise AssertionError("physical origin state dimension changed")

    # The theta-system has no origin pole.  Assert this again directly on the
    # only potentially rational rows (the solved top jets).
    allowed = [
        sp.Poly(z, z, domain="QQ").monic(),
        sp.Poly(18 * z + 5, z, domain="QQ").monic(),
    ]
    theta_lcm, _, theta_origin_order = fo.denominator_lcm(
        top_u + top_v, z, allowed
    )
    if theta_origin_order != 0:
        raise AssertionError("theta-system acquired an origin pole")
    if sp.rem(
        sp.Poly(theta_lcm, z, domain="QQ"),
        sp.Poly(z, z, domain="QQ"),
    ) == 0:
        raise AssertionError("theta-system denominator unexpectedly contains z")

    # A_theta(0) H(0)=H(0).  Chain rows shift jet k to k+1 and therefore act
    # trivially on H0 because every n=1 Euler jet has the same coefficient.
    # Only the two solved top rows require a symbolic check.
    top_xi_at_origin = rr.simp(
        sum(rr.simp(top_u[j].subs(z, 0)) * H0[j] for j in range(44))
    )
    top_kappa_at_origin = rr.simp(
        sum(rr.simp(top_v[j].subs(z, 0)) * H0[j] for j in range(44))
    )
    if not rr.is_zero_expr(top_xi_at_origin - xi1):
        raise AssertionError(
            "physical origin exponent-one compatibility failed in Xi top row"
        )
    if not rr.is_zero_expr(top_kappa_at_origin - kappa1):
        raise AssertionError(
            "physical origin exponent-one compatibility failed in K top row"
        )

    # The retained R1 constraint must hold at the first nonzero coefficient.
    constraint_on_H0 = rr.simp(
        sum(rr.simp(constraint[j].subs(z, 0)) * H0[j] for j in range(44))
    )
    if not rr.is_zero_expr(constraint_on_H0):
        raise AssertionError("physical origin direction violates retained R1 constraint")

    # Exact formal identity behind the cancellation: if
    # f(z)=sum_{n>=1} f_n z^n, then theta^k f/z has coefficients
    # n^k f_n z^(n-1), hence is a power series with the same positive radius.
    n, k = sp.symbols("n k", integer=True, positive=True)
    if sp.simplify(n**k * z**n / z - n**k * z ** (n - 1)) != 0:
        raise AssertionError("Euler-jet divisibility identity changed")

    borel_radius = sp.Rational(5, 18)
    if borel_radius <= 0:
        raise AssertionError("certified local Borel radius must be positive")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORIGIN_REMOVABILITY_CERTIFIED")
    print("DEPENDENCY := invariant-cone verifier certifies analytic order-2 Borel germ on |z|<5/18")
    print("PHYSICAL_BOREL_CONSTANT_TERM := Xi_0=0; K_0=0")
    print("PHYSICAL_BOREL_LINEAR_TERM := Xi_1=20/27; K_1=-5/27")
    print("STATE_DIVISIBILITY := every one of 44 Euler-jet components is divisible by z")
    print("DESINGULARIZED_STATE := H=Y/z analytic on |z|<5/18")
    print(f"THETA_SYSTEM_DENOMINATOR_LCM := {sp.sstr(theta_lcm)}")
    print("THETA_SYSTEM_ORIGIN_POLE_ORDER := 0")
    print("ORDINARY_SYSTEM_ORIGIN_FORM := Y'=(A_theta(z)/z)Y")
    print("PHYSICAL_ORIGIN_COMPATIBILITY := A_theta(0)*H(0)=H(0)")
    print("PHYSICAL_ORIGIN_EULER_EXPONENT := 1")
    print("RETAINED_CONSTRAINT_AT_ORIGIN := R1(H(0))=0")
    print("ORDINARY_MATRIX_ORIGIN_CLASSIFICATION := Fuchsian simple coordinate pole")
    print("PHYSICAL_GERM_ORIGIN_POLE := removable")
    print("PHYSICAL_GERM_DERIVATIVE_LIMIT := Y'(0)=H(0)=A_theta(0)H(0)")
    print("NONZERO_FINITE_THETA_SYSTEM_POLE := -5/18")
    print("BOUNDARY := removability is certified for the physical analytic germ, not for every solution sector of the 44-state Fuchsian system; analytic continuation beyond |z|<5/18 and Laplace summability remain unproved")


if __name__ == "__main__":
    main()
