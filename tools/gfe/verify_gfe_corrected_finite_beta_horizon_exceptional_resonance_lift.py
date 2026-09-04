#!/usr/bin/env python3
"""Certify the discrete exceptional beta_n resonance lift.

Scope: corrected AEH=1/2 Euler system, ell=2, lambda=6,
omega=i/(4M), alpha=1/2.  The nonresonant all-order recurrence loses its
adjacent-kernel coupling gamma_n on beta=beta_n.  This verifier proves that one
additional logarithmic degree supplies a nonzero derivative lift at every
integer resonance order n>=3.  It remains a formal-series result: no
convergence or horizon-to-r_c propagation is claimed.
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
    m = sp.symbols("m", integer=True, nonnegative=True)
    log_degree = sp.symbols("log_degree", integer=True, positive=True)
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

    resonance_den = sp.expand(12 * n * (n - 2) - 5)
    beta_n = simp(30 * M**2 * n * (n - 2) / resonance_den)
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
    resonance_source = matrix_simp(adjacent_res * r_prev)
    if simp((l_n.T * resonance_source)[0]) != 0:
        raise AssertionError("resonant adjacent-kernel source is not range-compatible")

    y_res = sp.Matrix([0, simp(-resonance_source[1] / kappa_res)])
    if not base._is_zero_matrix(matrix_simp(A_res * y_res + resonance_source)):
        raise AssertionError("resonant range lift y_n does not solve A_n y_n=-B1 r_{n-1}")

    # If the previous kernel coefficient is raised by one logarithmic degree,
    # solving its top-log range equation with y_res produces the next projected
    # derivative lift
    #
    #   delta_n = l_n^T [B0'(p_n)y_n + B1'(p_{n-1})r_{n-1}].
    #
    # A degree-d log monomial carries the nonzero scalar d*delta_n into the
    # next-lower log compatibility equation.
    derivative_lift_vector = matrix_simp(D0_res * y_res + D1_res * r_prev)
    delta_res = simp((l_n.T * derivative_lift_vector)[0])

    quartic = sp.expand(18 * n**4 - 170 * n**3 + 379 * n**2 - 277 * n + 30)
    expected_delta = simp(
        -75 * n * (n - 2) * quartic / resonance_den**2
    )
    if simp(delta_res - expected_delta) != 0:
        raise AssertionError(
            "exceptional resonance derivative lift changed; "
            f"actual={sp.sstr(delta_res)}"
        )

    # Exact integer nonvanishing certificate.  Directly check n=3..6.  For
    # n=m+7, m>=0, every coefficient of Q(m+7) is strictly positive.
    small_values = [sp.expand(quartic.subs(n, j)) for j in range(3, 7)]
    expected_small = [-522, -1286, -1880, -1380]
    if small_values != expected_small:
        raise AssertionError(
            "quartic small-order resonance classification changed; "
            f"actual={small_values}"
        )

    shifted_quartic = sp.expand(quartic.subs(n, m + 7))
    expected_shifted = 18 * m**4 + 334 * m**3 + 2101 * m**2 + 4735 * m + 1570
    if sp.expand(shifted_quartic - expected_shifted) != 0:
        raise AssertionError("shifted quartic positivity certificate changed")
    shifted_coeffs = sp.Poly(shifted_quartic, m).all_coeffs()
    if shifted_coeffs != [18, 334, 2101, 4735, 1570]:
        raise AssertionError("shifted quartic coefficients changed")
    if not all(int(c) > 0 for c in shifted_coeffs):
        raise AssertionError("shifted quartic lost coefficientwise positivity")

    # Mechanically verify the generic compatibility solver supplied by d*delta_n.
    # All previously fixed contributions at the next-lower log degree are an
    # arbitrary source S.  The extra previous-kernel amplitude tau is uniquely
    # fixed when d>=1 and delta_n!=0, after which the exact rank-one range solver
    # supplies the current coefficient.
    s0, s1, tau = sp.symbols("s0 s1 tau")
    S = sp.Matrix([s0, s1])
    projected_source = simp((l_n.T * S)[0])
    lifted_projection = simp(
        (l_n.T * (S + log_degree * tau * derivative_lift_vector))[0]
    )
    tau_solution = simp(-projected_source / (log_degree * delta_res))
    if simp(lifted_projection.subs(tau, tau_solution)) != 0:
        raise AssertionError("generalized-log resonance amplitude does not cancel compatibility")

    compatible_lifted_source = matrix_simp(
        (S + log_degree * tau * derivative_lift_vector).subs(tau, tau_solution)
    )
    current_particular = sp.Matrix(
        [0, simp(-compatible_lifted_source[1] / kappa_res)]
    )
    if not base._is_zero_matrix(
        matrix_simp(A_res * current_particular + compatible_lifted_source)
    ):
        raise AssertionError("generalized-log resonant compatible source lost range solution")

    # The resonance surfaces are pairwise distinct in the physical M>0 sector.
    # beta_n-beta_{n+1} has a strictly positive numerator and denominators for
    # every integer n>=3, so any fixed beta encounters at most one such order.
    beta_next = simp(
        30 * M**2 * (n + 1) * (n - 1) /
        (12 * (n + 1) * (n - 1) - 5)
    )
    resonance_spacing = simp(beta_n - beta_next)
    expected_spacing = simp(
        150 * M**2 * (2 * n - 1) /
        ((12 * n**2 - 24 * n - 5) * (12 * n**2 - 17))
    )
    if simp(resonance_spacing - expected_spacing) != 0:
        raise AssertionError("discrete resonance spacing formula changed")

    print("GFE_CORRECTED_FINITE_BETA_EXCEPTIONAL_DISCRETE_RESONANCE_LOG_LIFT_CERTIFIED")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/(4*M); alpha=1/2")
    print("RESONANCE_ORDER := integer n>=3")
    print("DISCRETE_RESONANCE_BETA_N := " + sp.sstr(beta_n))
    print("ADJACENT_KERNEL_COUPLING_ON_BETA_N := 0")
    print("RESONANT_RANGE_LIFT_Y_N := [" + ", ".join(sp.sstr(v) for v in y_res) + "]")
    print("DERIVATIVE_LIFT_DELTA_N := " + sp.sstr(delta_res))
    print("DELTA_QUARTIC_Q_N := " + sp.sstr(quartic))
    print("Q_3_TO_6 := " + sp.sstr(small_values))
    print("Q_M_PLUS_7 := " + sp.sstr(shifted_quartic) + " with m>=0")
    print("INTEGER_NONVANISHING := delta_n != 0 for every integer n>=3 under the nondegenerate M guard")
    print("LOG2_TO_LOG1_RESONANCE_STEP := uniquely solvable through 2*delta_n")
    print("LOG1_TO_ORDINARY_RESONANCE_STEP := uniquely solvable through delta_n")
    print("RESONANCE_SPACING := beta_n-beta_(n+1) = " + sp.sstr(resonance_spacing))
    print("PAIRWISE_DISTINCT_RESONANCES := certified for physical M>0 and integer n>=3")
    print("FORMAL_RESONANCE_CLASSIFICATION := each beta_n surface creates one extra logarithmic degree, not an obstruction")
    print("BOUNDARY := formal-series result only; convergence and horizon-to-r_c propagation remain open")
    print("NEXT_ROUTE := combine nonresonant induction with the single-resonance log lift, then attack convergence of the exceptional horizon series")


if __name__ == "__main__":
    main()
