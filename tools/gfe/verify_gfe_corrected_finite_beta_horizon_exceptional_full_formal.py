#!/usr/bin/env python3
"""Certify full formal exceptional horizon coverage for every physical beta>0.

Scope: corrected AEH=1/2 Euler system, ell=2, lambda=6,
omega=i/(4M), alpha=1/2.  This combines the exact nonresonant induction with
the discrete beta_n generalized-log lift.  The result is formal only: no
convergence, validated horizon data, horizon-to-r_c propagation, or C_phys
claim is made.
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

    corrected_prefactor = beta * (5 * M**2 + beta)
    kappa = simp(-corrected_prefactor * n * (n - 1) / (32 * M**5))
    c_n = sp.Matrix([-2 * M * (2 * n - 3), 1])
    d_n = sp.Matrix([-2 * M * (2 * n + 1), 1])
    if not base._is_zero_matrix(matrix_simp(A - kappa * c_n * d_n.T)):
        raise AssertionError("exceptional leading block factorization changed")

    if not base._is_zero_matrix(matrix_simp(A * r_n)):
        raise AssertionError("exceptional right kernel changed")
    if not base._is_zero_matrix(matrix_simp(l_n.T * A)):
        raise AssertionError("exceptional left projector changed")

    coupling_bracket = simp(
        30 * M**2 * n * (n - 2) - (12 * n * (n - 2) - 5) * beta
    )
    gamma = simp((l_n.T * adjacent * r_prev)[0])
    expected_gamma = simp(
        -2 * beta * (n - 1) ** 2 * coupling_bracket / (3 * M**4)
    )
    if simp(gamma - expected_gamma) != 0:
        raise AssertionError("exceptional adjacent-kernel coupling changed")

    log_kernel_decoupling = simp((l_n.T * D0 * r_n)[0])
    if log_kernel_decoupling != 0:
        raise AssertionError("current kernel freedom re-entered lower-log compatibility")

    # ------------------------------------------------------------------
    # Nonresonant triangular step, valid independently at each active log
    # degree.  The arbitrary source S absorbs all already-known contributions
    # from higher logarithmic degrees and lower radial lags.  The previous
    # same-degree kernel amplitude enters through gamma_n and is uniquely fixed
    # whenever gamma_n != 0.  The exact rank-one range solver then closes the
    # full vector equation.  We verify this separately for log degrees 2, 1, 0.
    # ------------------------------------------------------------------
    nonresonant_solutions = []
    for degree in (2, 1, 0):
        s0, s1, rho = sp.symbols(f"s{degree}_0 s{degree}_1 rho{degree}")
        S = sp.Matrix([s0, s1])
        source = matrix_simp(S + rho * adjacent * r_prev)
        projection = simp((l_n.T * source)[0])
        rho_solution = simp(-((l_n.T * S)[0]) / gamma)
        if simp(projection.subs(rho, rho_solution)) != 0:
            raise AssertionError(
                f"nonresonant compatibility failed at log degree {degree}"
            )
        compatible = matrix_simp(source.subs(rho, rho_solution))
        particular = sp.Matrix([0, simp(-compatible[1] / kappa)])
        if not base._is_zero_matrix(matrix_simp(A * particular + compatible)):
            raise AssertionError(
                f"nonresonant range solve failed at log degree {degree}"
            )
        nonresonant_solutions.append((degree, rho_solution))

    # A fresh current kernel amplitude at degree d contributes d*D0*r_n to the
    # next-lower log equation.  Its projector vanishes for both possible active
    # transitions 2->1 and 1->0, preserving the triangular induction.
    for degree in (2, 1):
        if simp(degree * (l_n.T * D0 * r_n)[0]) != 0:
            raise AssertionError(
                f"current degree-{degree} kernel freedom spoils triangularity"
            )

    # ------------------------------------------------------------------
    # Discrete resonance case beta=beta_n.  gamma_n vanishes, but the previous
    # kernel source lies in range(A_n).  Solving that top-log equation exposes
    # the derivative lift delta_n.  Its exact integer nonvanishing means one
    # extra logarithmic degree restores each lost compatibility scalar.
    # ------------------------------------------------------------------
    resonance_den = sp.expand(12 * n * (n - 2) - 5)
    beta_n = simp(30 * M**2 * n * (n - 2) / resonance_den)
    resonant = {beta: beta_n}

    A_res = matrix_simp(A.subs(resonant))
    adjacent_res = matrix_simp(adjacent.subs(resonant))
    D0_res = matrix_simp(D0.subs(resonant))
    D1_res = matrix_simp(D1.subs(resonant))
    gamma_res = simp((l_n.T * adjacent_res * r_prev)[0])
    if gamma_res != 0:
        raise AssertionError("beta_n no longer defines the discrete resonance")

    kappa_res = simp(kappa.subs(resonant))
    resonance_source = matrix_simp(adjacent_res * r_prev)
    if simp((l_n.T * resonance_source)[0]) != 0:
        raise AssertionError("resonant previous-kernel source left the leading range")

    y_res = sp.Matrix([0, simp(-resonance_source[1] / kappa_res)])
    if not base._is_zero_matrix(matrix_simp(A_res * y_res + resonance_source)):
        raise AssertionError("resonant top-log range lift failed")

    derivative_lift = matrix_simp(D0_res * y_res + D1_res * r_prev)
    delta = simp((l_n.T * derivative_lift)[0])
    quartic = sp.expand(18 * n**4 - 170 * n**3 + 379 * n**2 - 277 * n + 30)
    expected_delta = simp(-75 * n * (n - 2) * quartic / resonance_den**2)
    if simp(delta - expected_delta) != 0:
        raise AssertionError("resonant derivative lift changed")

    # Exact nonvanishing for every integer n>=3: n=3..6 are explicit nonzero
    # values, and Q(m+7) has strictly positive coefficients for m>=0.
    small_values = [sp.expand(quartic.subs(n, j)) for j in range(3, 7)]
    if small_values != [-522, -1286, -1880, -1380]:
        raise AssertionError("resonant quartic small-order classification changed")
    shifted_quartic = sp.expand(quartic.subs(n, m + 7))
    expected_shifted = 18 * m**4 + 334 * m**3 + 2101 * m**2 + 4735 * m + 1570
    if sp.expand(shifted_quartic - expected_shifted) != 0:
        raise AssertionError("resonant quartic shifted positivity identity changed")
    shifted_coeffs = sp.Poly(shifted_quartic, m).all_coeffs()
    if shifted_coeffs != [18, 334, 2101, 4735, 1570]:
        raise AssertionError("resonant quartic positivity coefficients changed")

    # Mechanically close the two compatibility equations created by the one
    # log-degree escalation.  Degree 2 repairs the log-1 equation through
    # 2*delta_n; degree 1 repairs the ordinary equation through delta_n.
    resonance_repairs = []
    for degree in (2, 1):
        s0, s1, tau = sp.symbols(f"rs{degree}_0 rs{degree}_1 tau{degree}")
        S = sp.Matrix([s0, s1])
        source = matrix_simp(S + degree * tau * derivative_lift)
        projection = simp((l_n.T * source)[0])
        tau_solution = simp(-((l_n.T * S)[0]) / (degree * delta))
        if simp(projection.subs(tau, tau_solution)) != 0:
            raise AssertionError(
                f"resonant generalized-log compatibility failed at degree {degree}"
            )
        compatible = matrix_simp(source.subs(tau, tau_solution))
        particular = sp.Matrix([0, simp(-compatible[1] / kappa_res)])
        if not base._is_zero_matrix(matrix_simp(A_res * particular + compatible)):
            raise AssertionError(
                f"resonant generalized-log range solve failed at degree {degree}"
            )
        resonance_repairs.append((degree, tau_solution))

    # The resonance sequence is strictly decreasing for physical M>0 and
    # integer n>=3, hence a fixed beta>0 can hit at most one resonance order.
    beta_next = simp(
        30 * M**2 * (n + 1) * (n - 1) /
        (12 * (n + 1) * (n - 1) - 5)
    )
    spacing = simp(beta_n - beta_next)
    expected_spacing = simp(
        150 * M**2 * (2 * n - 1) /
        ((12 * n**2 - 24 * n - 5) * (12 * n**2 - 17))
    )
    if simp(spacing - expected_spacing) != 0:
        raise AssertionError("resonance spacing formula changed")

    # Denominators in beta_n and the spacing are positive for n>=3.  Encode the
    # integer shift identities used to certify this without a numerical grid.
    den_shift = sp.expand(resonance_den.subs(n, m + 3))
    next_den_shift = sp.expand((12 * n**2 - 17).subs(n, m + 3))
    if den_shift != 12 * m**2 + 48 * m + 31:
        raise AssertionError("resonance denominator positivity shift changed")
    if next_den_shift != 12 * m**2 + 72 * m + 91:
        raise AssertionError("next resonance denominator positivity shift changed")

    print("GFE_CORRECTED_FINITE_BETA_EXCEPTIONAL_FULL_FORMAL_HORIZON_CERTIFIED")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/(4*M); alpha=1/2")
    print("NONRESONANT_GAMMA_N := " + sp.sstr(gamma))
    print("DISCRETE_RESONANCE_BETA_N := " + sp.sstr(beta_n) + " for integer n>=3")
    print("RESONANCE_DERIVATIVE_LIFT_DELTA_N := " + sp.sstr(delta))
    print("RESONANCE_DELTA_INTEGER_NONVANISHING := certified for every integer n>=3")
    print("PAIRWISE_DISTINCT_RESONANCES := certified for physical M>0")
    print("FIXED_BETA_RESONANCE_COUNT := at most one")
    print("OFF_RESONANCE_MAX_LOG_DEGREE := 1")
    print("ON_RESONANCE_MAX_LOG_DEGREE := 2")
    print("POST_RESONANCE_TRIANGULAR_PROPAGATION := certified at log degrees 2,1,0")
    print("FORMAL_EXCEPTIONAL_FINITE_BETA_HORIZON := all-order for every physical M>0, beta>0")
    print("NONDEGENERATE_GUARD := M>0 and beta>0, hence M*beta*(5*M^2+beta)!=0")
    print("NO_CONVERGENCE_CLAIM := True")
    print("BOUNDARY := no validated horizon initial state; no horizon-to-r_c map; no C_phys; no global Chronos closure")
    print("NEXT_ROUTE := classify coefficient growth and prove convergence of the exceptional horizon Frobenius series")


if __name__ == "__main__":
    main()
