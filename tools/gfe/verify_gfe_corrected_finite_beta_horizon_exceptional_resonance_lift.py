#!/usr/bin/env python3
"""Audit the discrete exceptional beta_n resonance surfaces.

Scope: corrected AEH=1/2 Euler system, ell=2, lambda=6,
omega=i/(4M), alpha=1/2.  The nonresonant all-order recurrence loses its
adjacent-kernel coupling gamma_n on beta=beta_n.  This verifier computes the
next generalized-log derivative lift exactly, directly from the Euler artifact.
It does not claim convergence or horizon-to-r_c propagation.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def matrix_simp(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


def laurent_coeff(expr: sp.Expr, x: sp.Symbol, power: int) -> sp.Expr:
    return simp(sp.residue(sp.together(expr / x ** (power + 1)), x, 0))


def main() -> None:
    equations, h = base._parse_equations()

    M = base.M
    beta = base.beta
    lam = base.lam
    omega = base.omega
    r = base.r
    I = base.I
    p = base.p

    x = sp.symbols("x", positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    a, b = sp.symbols("a b")

    trial = {}
    for order in range(5):
        trial[h[0][order]] = a * base._falling(p, order) / x**order
        trial[h[1][order]] = b * base._falling(p - 1, order) / x ** (order + 1)

    specialized = []
    for equation in equations:
        q = equation.xreplace(trial)
        q = q.subs({r: 2 * M + x, omega: I / (4 * M), lam: 6})
        specialized.append(simp(q))

    q0, q1 = specialized

    def block(lag: int) -> sp.Matrix:
        row0 = laurent_coeff(q0, x, -3 + lag)
        row1 = laurent_coeff(q1, x, -2 + lag)
        return matrix_simp(
            sp.Matrix(
                [
                    [sp.diff(row0, a), sp.diff(row0, b)],
                    [sp.diff(row1, a), sp.diff(row1, b)],
                ]
            )
        )

    B0 = block(0)
    B1 = block(1)

    alpha = sp.Rational(1, 2)
    pn = alpha + n
    pprev = alpha + n - 1

    A = matrix_simp(B0.subs(p, pn))
    adjacent = matrix_simp(B1.subs(p, pprev))
    D0 = matrix_simp(B0.diff(p).subs(p, pn))
    D1 = matrix_simp(B1.diff(p).subs(p, pprev))

    r_n = sp.Matrix([1, 2 * M * (2 * n + 1)])
    l_n = sp.Matrix([1, 2 * M * (2 * n - 3)])
    r_prev = sp.Matrix([1, 2 * M * (2 * n - 1)])

    beta_n = simp(30 * M**2 * n * (n - 2) / (12 * n * (n - 2) - 5))
    substitutions = {beta: beta_n}

    A_res = matrix_simp(A.subs(substitutions))
    adjacent_res = matrix_simp(adjacent.subs(substitutions))
    D0_res = matrix_simp(D0.subs(substitutions))
    D1_res = matrix_simp(D1.subs(substitutions))

    gamma_res = simp((l_n.T * adjacent_res * r_prev)[0])
    if gamma_res != 0:
        raise AssertionError(
            "classified beta_n surface no longer kills adjacent-kernel coupling; "
            f"gamma={sp.sstr(gamma_res)}"
        )

    corrected_prefactor_res = simp(beta_n * (5 * M**2 + beta_n))
    kappa_res = simp(-corrected_prefactor_res * n * (n - 1) / (32 * M**5))

    # On gamma_n=0, the adjacent previous-kernel source lies in range(A_n).
    # Solve A_n y_n = -B1(p_{n-1}) r_{n-1} with the same exact rank-one
    # range solver used in the nonresonant induction.
    resonance_source = matrix_simp(adjacent_res * r_prev)
    if simp((l_n.T * resonance_source)[0]) != 0:
        raise AssertionError("resonant adjacent-kernel source is not range-compatible")

    y_res = sp.Matrix([0, simp(-resonance_source[1] / kappa_res)])
    if not base._is_zero_matrix(matrix_simp(A_res * y_res + resonance_source)):
        raise AssertionError("resonant range lift y_n does not solve A_n y_n=-B1 r_{n-1}")

    # Raising the previous coefficient by one logarithmic degree produces,
    # after solving the top-log range equation, the next projected lift
    #
    #   delta_n = l_n^T [ B0'(p_n) y_n + B1'(p_{n-1}) r_{n-1} ].
    #
    # A nonzero delta_n means the resonance does not obstruct the formal
    # branch: the extra log-degree amplitude replaces the vanished gamma_n.
    derivative_lift_vector = matrix_simp(D0_res * y_res + D1_res * r_prev)
    delta_res = simp((l_n.T * derivative_lift_vector)[0])
    if delta_res == 0:
        raise AssertionError(
            "first generalized-log derivative lift vanishes identically on beta_n; "
            "a higher lift is required"
        )

    numerator, denominator = sp.fraction(sp.cancel(delta_res))
    numerator = sp.factor(numerator)
    denominator = sp.factor(denominator)

    print("GFE_CORRECTED_FINITE_BETA_EXCEPTIONAL_DISCRETE_RESONANCE_LIFT_AUDIT")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/(4*M); alpha=1/2")
    print("RESONANCE_ORDER := integer n>=3")
    print("DISCRETE_RESONANCE_BETA_N := " + sp.sstr(beta_n))
    print("ADJACENT_KERNEL_COUPLING_ON_BETA_N := 0")
    print("RESONANT_RANGE_LIFT_Y_N := [" + ", ".join(sp.sstr(v) for v in y_res) + "]")
    print("DERIVATIVE_LIFT_DELTA_N := " + sp.sstr(delta_res))
    print("DERIVATIVE_LIFT_NUMERATOR := " + sp.sstr(numerator))
    print("DERIVATIVE_LIFT_DENOMINATOR := " + sp.sstr(denominator))
    print("STRUCTURAL_INTERPRETATION := one additional log degree is the first candidate replacement for vanished gamma_n")
    print("BOUNDARY := nonvanishing for every integer n>=3 not yet classified; no convergence or global propagation claim")
    print("NEXT_ROUTE := classify zeros of delta_n for integer n>=3 and certify generalized-log resonance solvability if none occur")


if __name__ == "__main__":
    main()
