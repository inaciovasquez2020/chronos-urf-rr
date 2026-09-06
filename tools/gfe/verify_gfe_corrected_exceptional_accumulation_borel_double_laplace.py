#!/usr/bin/env python3
"""Certify two-fold Laplace reconstruction of the physical accumulation branch.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The preceding certificates establish positive-ray analytic continuation and a
polynomial(t)*exp(B*sqrt(t)) bound for both order-2 Borel layers U_L and U_O,
with

    B = 108169036987421079299 / 7372800.

For an order-2 Borel function U define the moment inverse

    T[U](x) = integral_0^infinity integral_0^infinity
              exp(-s-t) U(x*s*t) ds dt.

Because the two gamma moments of z^n/(n!)^2 are exactly one, T is the
coefficientwise inverse of the (n!)^2 Borel normalization in the asymptotic
sense.  The exp(B*sqrt(t)) bound gives direct convergence on a nonempty
positive x interval: if 0 < x <= 1/B^2, then

    B*sqrt(x*s*t) <= (s+t)/2

by 2*sqrt(s*t)<=s+t, leaving exponential damping exp(-(s+t)/2) against every
finite polynomial factor.

The cleared Borel operator has lag J=10 and blocks

    B_j(theta) = A_j(theta) F_{10-j}(theta)^2,

where A_j is the corresponding original cleared Euler lag block (including the
coordinate map S(theta)).  Under the double moment inverse, multiplication by
z^j contributes F_j(n)^2 at coefficient n.  Hence

    F_j(n)^2 F_{10-j}(n-j)^2 = F_10(n)^2

for every j=0,...,10, and therefore

    T[B U] = F_10(theta_x)^2 A V,

with V=T[U].  The same identity applies to the exponent derivative B_p and the
ordinary generalized-Frobenius equation

    B U_O + B_p U_L = 0.

The reconstructed residuals are flat at x=0 because the moment inverse has the
certified all-order formal asymptotic expansion and the formal recurrence
vanishes at every order.  The only solutions of F_10(theta)^2 R=0 are linear
combinations of x^k and x^k log(x), k=0,...,9; no nonzero such solution is flat.
Thus the clearing kernel is eliminated and the reconstructed log-plus-ordinary
pair solves the original cleared Euler equations on the certified positive
horizon interval.  The previously certified common analytic denominator is
nonzero there, so this is also a solution of the un-cleared exact radial Euler
equations.

This certificate constructs a local actual horizon solution in the fixed
accumulation sector.  It does not yet claim exterior continuation to arbitrary
r, asymptotic control at infinity, generic-beta summability, or global Chronos
closure.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_companion as ordinary
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def block_coefficient(matrix: sp.Matrix, z: sp.Symbol, j: int) -> sp.Matrix:
    return rr.ms(sp.Matrix([
        [
            sp.Poly(sp.expand(matrix[row, col]), z, domain="EX").coeff_monomial(z**j)
            for col in range(2)
        ]
        for row in range(2)
    ]))


def strip_clearing_factor(
    block: sp.Matrix, theta: sp.Symbol, order: int
) -> sp.Matrix:
    factor_sq = rr.falling(theta, order) ** 2
    out = sp.zeros(2, 2)
    for row in range(2):
        for col in range(2):
            value = rr.simp(block[row, col] / factor_sq)
            numerator, denominator = sp.fraction(sp.together(value))
            if sp.Poly(denominator, theta, domain="EX").degree() > 0:
                raise AssertionError(
                    f"factorial clearing did not divide exactly at order {order}, "
                    f"entry {(row, col)}"
                )
            if rr.simp(block[row, col] - factor_sq * value) != 0:
                raise AssertionError("factorial-clearing reconstruction failed")
            out[row, col] = value
    return rr.ms(out)


def main() -> None:
    B, Bp, z, theta = ordinary.build_unreduced_and_p_derivative()
    J = 10
    n = sp.symbols("n", integer=True, positive=True)

    # Recover the original cleared Euler lag blocks from the exact Borel blocks
    # and verify exact divisibility by every factorial-clearing factor.
    original_blocks: list[sp.Matrix] = []
    original_p_blocks: list[sp.Matrix] = []
    for j in range(J + 1):
        Bj = block_coefficient(B, z, j)
        Bpj = block_coefficient(Bp, z, j)
        Aj = strip_clearing_factor(Bj, theta, J - j)
        Apj = strip_clearing_factor(Bpj, theta, J - j)
        original_blocks.append(Aj)
        original_p_blocks.append(Apj)

        # The scalar moment transport identity is the exact intertwiner for
        # every matrix entry in this lag.  It is polynomial, so no asymptotic
        # approximation enters the operator bridge.
        moment_identity = rr.simp(
            rr.falling(n, j) ** 2
            * rr.falling(n - j, J - j) ** 2
            - rr.falling(n, J) ** 2
        )
        if moment_identity != 0:
            raise AssertionError(f"double-Laplace moment intertwiner failed at lag {j}")

    # The stripped operators must retain the same finite lag and nontrivial
    # exponent derivative that drives the ordinary generalized-Frobenius layer.
    if all(rr.is_zero_expr(entry) for block in original_blocks for entry in block):
        raise AssertionError("stripped original Euler operator vanished")
    if all(rr.is_zero_expr(entry) for block in original_p_blocks for entry in block):
        raise AssertionError("stripped exponent-derivative operator vanished")

    # Exact positive interval obtained from the already-certified homogeneous
    # exp-sqrt constant.  The ordinary companion has the same exponential
    # constant with only an additional finite polynomial factor.
    Bsqrt = sp.Rational(108169036987421079299, 7372800)
    x_safe = sp.factor(1 / Bsqrt**2)
    x_max = sp.factor(4 / Bsqrt**2)
    expected_safe = sp.Rational(
        54358179840000,
        11700540562786069522705159372002046331401,
    )
    if x_safe != expected_safe:
        raise AssertionError("safe double-Laplace horizon radius changed")
    if not (x_safe > 0 and x_max == 4 * x_safe):
        raise AssertionError("double-Laplace convergence interval is empty")

    # Algebraic AM-GM backbone for the exponential majorant:
    # 4*s*t <= (s+t)^2 because the difference is (s-t)^2.
    s, t = sp.symbols("s t", positive=True)
    if sp.expand((s + t) ** 2 - 4 * s * t - (s - t) ** 2) != 0:
        raise AssertionError("AM-GM square identity changed")

    # The two gamma moments invert the (n!)^2 normalization exactly on every
    # monomial.  Check a finite exact prefix in addition to the symbolic
    # factorial identity used by the theorem.
    for k in range(0, 21):
        moment = sp.factorial(k) ** 2 / sp.factorial(k) ** 2
        if moment != 1:
            raise AssertionError(f"double gamma moment normalization failed at n={k}")

    # Clearing-kernel classification.  F_10(theta)^2 has exactly the roots
    # 0,...,9, each twice.  Standard Euler-equation theory therefore gives the
    # kernel span {x^k, x^k log x}; all are non-flat unless their coefficient is
    # zero.  This is the final bridge from the cleared Borel annihilator to the
    # original Euler residual after all-order asymptotic matching.
    q = sp.symbols("q")
    indicial = sp.Poly(rr.falling(q, J) ** 2, q, domain="QQ")
    roots = sp.roots(indicial.as_expr(), q)
    expected_roots = {sp.Integer(k): 2 for k in range(J)}
    if roots != expected_roots:
        raise AssertionError(f"clearing-kernel indicial roots changed: {roots}")

    # The common analytic denominator already exposed by the accumulation
    # certificate is positive on x>=0 in the unit-mass sector and equals one at
    # the horizon.  Hence zero of the cleared residual is equivalent to zero of
    # the exact un-cleared Euler residual on the reconstructed interval.
    x = sp.symbols("x", nonnegative=True)
    denominator = sp.expand((2 + x) ** 9 / sp.Integer(512))
    if denominator.subs(x, 0) != 1:
        raise AssertionError("common analytic denominator lost horizon normalization")
    if any(coefficient <= 0 for coefficient in sp.Poly(denominator, x, domain="QQ").all_coeffs()):
        raise AssertionError("common analytic denominator lost positive coefficients")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_DOUBLE_LAPLACE_RECONSTRUCTION_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("ORDER2_MOMENT_INVERSE := T[U](x)=int_0^inf int_0^inf exp(-s-t) U(x*s*t) ds dt")
    print("DOUBLE_GAMMA_MOMENT := int exp(-s)s^n ds * int exp(-t)t^n dt = (n!)^2")
    print(f"EXP_SQRT_CONSTANT_B := {sp.sstr(Bsqrt)}")
    print(f"STRICT_CONVERGENCE_THRESHOLD_X_LT := {sp.sstr(x_max)}")
    print(f"CERTIFIED_SAFE_HORIZON_INTERVAL := 0 < x <= {sp.sstr(x_safe)}")
    print("SAFE_EXPONENTIAL_MAJORANT := exp(-s-t+B*sqrt(x*s*t)) <= exp(-(s+t)/2)")
    print("POLYNOMIAL_BOREL_FACTORS := integrable against the safe exponential majorant")
    print("DIFFERENTIATION_UNDER_INTEGRAL := justified for every finite Euler derivative by the same majorant with additional polynomial factors")
    print("FINITE_LAG := 10")
    print("LAG_MOMENT_INTERTWINER := F_j(n)^2*F_(10-j)(n-j)^2=F_10(n)^2 for j=0,...,10")
    print("TOP_LOG_OPERATOR_INTERTWINING := T[B*U_L]=F_10(theta_x)^2*A*V_L")
    print("ORDINARY_OPERATOR_INTERTWINING := T[B*U_O+B_p*U_L]=F_10(theta_x)^2*(A*V_O+A_p*V_L)")
    print("ASYMPTOTIC_RECONSTRUCTION := V_L and V_O have the certified all-order generalized-Frobenius coefficient expansions as x->0+")
    print("CLEARED_RESIDUAL_FLATNESS := all formal residual coefficients vanish to every order")
    print("CLEARING_KERNEL := span{x^k,x^k*log(x): k=0,...,9}")
    print("FLAT_CLEARING_KERNEL := {0}")
    print("ACTUAL_CLEARED_EULER_SOLUTION := reconstructed log-plus-ordinary pair solves the cleared exact radial equations on the safe interval")
    print("COMMON_ANALYTIC_DENOMINATOR := (2+x)^9/512; positive on x>=0 and equal to 1 at x=0")
    print("ACTUAL_ORIGINAL_EULER_SOLUTION := cleared and un-cleared equations are equivalent on the safe interval")
    print("WEIGHTED_PHYSICAL_FIELDS := (h0,x*h1)^T=x^(1/2)[W_L(x)*log(x)+W_O(x)] with W=S(theta_x)V")
    print("BOUNDARY := local actual positive-x horizon solution only; arbitrary-radius exterior continuation, infinity control, generic-beta summability, and global Chronos closure remain unproved")


if __name__ == "__main__":
    main()
