#!/usr/bin/env python3
"""Re-derive the exceptional omega=i/(4M), ell=2 horizon recurrence
from the corrected AEH=1/2 Euler artifact.

Historical exceptional-frequency certificates are not imported as proofs here:
the corrected finite-beta descriptor has a finite-radius rank-loss surface, so
source binding must be re-established directly.  This verifier constructs the
row-scaled Frobenius blocks from
artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json and checks the
exceptional logarithmic recurrence against exact formulas.
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

    x = sp.symbols("x", positive=True)
    p = base.p
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
    B2 = block(2)

    alpha = sp.Rational(1, 2)
    pn = alpha + n
    A = matrix_simp(B0.subs(p, pn))

    # The corrected AEH=1/2 source preserves the historical rank-one block
    # shape but changes its overall coefficient from beta^2 to
    # beta*(5*M^2+beta).  This normalization is derived from the corrected
    # artifact and is not imported from the historical source.
    corrected_prefactor = beta * (5 * M**2 + beta)
    expected_A = sp.Matrix(
        [
            [
                -corrected_prefactor * n * (n - 1) * (2 * n - 3) * (2 * n + 1) / (8 * M**3),
                corrected_prefactor * n * (n - 1) * (2 * n - 3) / (16 * M**4),
            ],
            [
                corrected_prefactor * n * (n - 1) * (2 * n + 1) / (16 * M**4),
                -corrected_prefactor * n * (n - 1) / (32 * M**5),
            ],
        ]
    )
    if not base._is_zero_matrix(matrix_simp(A - expected_A)):
        raise AssertionError(
            "corrected exceptional leading block changed after normalization repair; "
            f"actual={A.tolist()}"
        )

    r_n = sp.Matrix([1, 2 * M * (2 * n + 1)])
    l_n = sp.Matrix([1, 2 * M * (2 * n - 3)])
    r_prev = sp.Matrix([1, 2 * M * (2 * n - 1)])
    if not base._is_zero_matrix(matrix_simp(A * r_n)):
        raise AssertionError("corrected exceptional right kernel changed")
    if not base._is_zero_matrix(matrix_simp(l_n.T * A)):
        raise AssertionError("corrected exceptional left projector changed")

    adjacent = matrix_simp(B1.subs(p, alpha + n - 1))
    gamma = simp((l_n.T * adjacent * r_prev)[0])
    expected_gamma = simp(
        -2
        * beta
        * (n - 1) ** 2
        * (6 * (5 * M**2 - 2 * beta) * n * (n - 2) + 5 * beta)
        / (3 * M**4)
    )
    if simp(gamma - expected_gamma) != 0:
        raise AssertionError(
            "corrected exceptional adjacent kernel coupling changed after exact repair; "
            f"actual={sp.sstr(gamma)}"
        )

    D_nn = matrix_simp(B0.diff(p).subs(p, pn))
    if simp((l_n.T * D_nn * r_n)[0]) != 0:
        raise AssertionError("corrected exceptional log-kernel decoupling changed")

    p0 = alpha
    p1 = alpha + 1
    p2 = alpha + 2
    B0_p0 = matrix_simp(B0.subs(p, p0))
    B0_p1 = matrix_simp(B0.subs(p, p1))
    B0_p2 = matrix_simp(B0.subs(p, p2))
    if not base._is_zero_matrix(B0_p0) or not base._is_zero_matrix(B0_p1):
        raise AssertionError("corrected exceptional double resonance changed")
    if simp(B0_p2.det()) != 0 or B0_p2.rank() != 1:
        raise AssertionError("corrected exceptional n=2 rank-one block changed")

    # Normalize the leading ordinary amplitude to the branch already used by
    # the corrected generic horizon audit: u0=(1,2M).  The exceptional one-log
    # amplitude is then fixed by the exact order-one equation.
    c1 = sp.Rational(5, 3) / M
    u0 = sp.Matrix([1, 2 * M])
    v1 = c1 * sp.Matrix([1, -2 * M])
    order1 = matrix_simp(B1.subs(p, p0) * u0 + B0.diff(p).subs(p, p1) * v1)
    if not base._is_zero_matrix(order1):
        raise AssertionError(
            "exceptional one-log correction does not cancel the corrected n=1 source; "
            f"residual={order1.tolist()}"
        )

    l2 = sp.Matrix([1, 2 * M])
    log2_source = matrix_simp(B1.subs(p, p1) * v1)
    if simp((l2.T * log2_source)[0]) != 0:
        raise AssertionError("exceptional order-two log compatibility failed")

    v2_part = sp.Matrix(
        [
            -2 * c1 * (36 * M**4 - 19 * beta**2) / (15 * M * beta**2),
            0,
        ]
    )
    log2_residual = matrix_simp(B0_p2 * v2_part + log2_source)
    if not base._is_zero_matrix(log2_residual):
        raise AssertionError(
            "exceptional order-two logarithmic correction changed; "
            f"residual={log2_residual.tolist()}"
        )

    a1 = sp.symbols("a1")
    u1 = sp.Matrix([a1, -2 * M * a1 - sp.Rational(362, 25) * M * c1])
    nonlog2_source = matrix_simp(
        B1.subs(p, p1) * u1
        + B2.subs(p, p0) * u0
        + B0.diff(p).subs(p, p2) * v2_part
        + B1.diff(p).subs(p, p1) * v1
    )
    if simp((l2.T * nonlog2_source)[0]) != 0:
        raise AssertionError(
            "exceptional total-order-two ordinary compatibility failed; "
            f"pairing={sp.sstr(simp((l2.T * nonlog2_source)[0]))}"
        )

    m = sp.symbols("m", integer=True, nonnegative=True)
    shifted = sp.expand(
        (6 * (5 * M**2 - 2 * beta) * n * (n - 2) + 5 * beta).subs(n, m + 3)
    )
    expected_shifted = sp.expand(
        6 * (5 * M**2 - 2 * beta) * (m + 3) * (m + 1) + 5 * beta
    )
    if sp.expand(shifted - expected_shifted) != 0:
        raise AssertionError("corrected exceptional shifted coupling identity changed")

    compatibility_det = simp(gamma**2)

    print("GFE_CORRECTED_FINITE_BETA_EXCEPTIONAL_HORIZON_FORMAL_RECURRENCE")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/(4*M); alpha=1/2")
    print("CORRECTED_LEADING_PREFACTOR := beta*(5*M^2+beta)")
    print("NORMALIZED_LEADING_SEED := [1, 2*M]")
    print("FORCED_FIRST_LOG_COEFFICIENT := [5/(3*M), -10/3]")
    print("ORDER_N_RIGHT_KERNEL := [1, 2*M*(2*n+1)]")
    print("ORDER_N_LEFT_PROJECTOR := [1, 2*M*(2*n-3)]")
    print("ADJACENT_KERNEL_COUPLING := " + sp.sstr(gamma))
    print("LOG_KERNEL_DECOUPLING := 0")
    print("ORDER_TWO_COMPATIBILITY := passed")
    print("COMPATIBILITY_DETERMINANT := " + sp.sstr(compatibility_det))
    print("BOUNDARY := nonvanishing of the corrected adjacent coupling for the intended beta domain is not yet proved")
    print("FORMAL_EXCEPTIONAL_LOG_FROBENIUS := not yet promoted to every Laurent order")
    print("NEXT_ROUTE := derive the first corrected low-order coefficient mismatch, then prove the corrected coupling nonvanishing domain")


if __name__ == "__main__":
    main()
