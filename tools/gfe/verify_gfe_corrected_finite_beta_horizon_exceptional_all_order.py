#!/usr/bin/env python3
"""Certify the all-order exceptional formal Frobenius recurrence mechanism.

Scope: corrected AEH=1/2 Euler system, ell=2, lambda=6,
omega=i/(4M), alpha=1/2.  This verifier does not claim convergence.
It proves the exact algebraic induction step for every n>=3 away from the
discrete adjacent-kernel resonance surfaces classified by the exceptional
recurrence audit.
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
    D = matrix_simp(B0.diff(p).subs(p, pn))

    corrected_prefactor = beta * (5 * M**2 + beta)
    kappa = simp(-corrected_prefactor * n * (n - 1) / (32 * M**5))
    c_n = sp.Matrix([-2 * M * (2 * n - 3), 1])
    d_n = sp.Matrix([-2 * M * (2 * n + 1), 1])
    outer = matrix_simp(kappa * c_n * d_n.T)
    if not base._is_zero_matrix(matrix_simp(A - outer)):
        raise AssertionError("exceptional leading block lost rank-one outer factorization")

    r_n = sp.Matrix([1, 2 * M * (2 * n + 1)])
    l_n = sp.Matrix([1, 2 * M * (2 * n - 3)])
    r_prev = sp.Matrix([1, 2 * M * (2 * n - 1)])
    if not base._is_zero_matrix(matrix_simp(A * r_n)):
        raise AssertionError("exceptional current right kernel changed")
    if not base._is_zero_matrix(matrix_simp(l_n.T * A)):
        raise AssertionError("exceptional current left projector changed")

    gamma = simp((l_n.T * adjacent * r_prev)[0])
    coupling_bracket = simp(
        30 * M**2 * n * (n - 2) - (12 * n * (n - 2) - 5) * beta
    )
    expected_gamma = simp(
        -2 * beta * (n - 1) ** 2 * coupling_bracket / (3 * M**4)
    )
    if simp(gamma - expected_gamma) != 0:
        raise AssertionError("exceptional adjacent-kernel coupling changed")

    beta_n = simp(
        30 * M**2 * n * (n - 2) / (12 * n * (n - 2) - 5)
    )
    if simp(coupling_bracket.subs(beta, beta_n)) != 0:
        raise AssertionError("exceptional discrete resonance surface changed")

    log_kernel_decoupling = simp((l_n.T * D * r_n)[0])
    if log_kernel_decoupling != 0:
        raise AssertionError("current log-kernel freedom re-entered ordinary compatibility")

    # Rank-one range solver.  If l_n^T S=0 then S is proportional to c_n,
    # and y=[0,-S_2/kappa] solves A_n y + S = 0.  Verify this exact formula
    # symbolically on a generic compatible source.
    s1 = sp.symbols("s1")
    compatible_source = sp.Matrix([-2 * M * (2 * n - 3) * s1, s1])
    range_solution = sp.Matrix([0, simp(-s1 / kappa)])
    if not base._is_zero_matrix(matrix_simp(A * range_solution + compatible_source)):
        raise AssertionError("exceptional rank-one compatible-source solver changed")

    # Log induction step.  All already-known lagged terms are represented by
    # an arbitrary source S.  The only not-yet-fixed coefficient from order
    # n-1 is rho_{n-1} r_{n-1}; its projector coefficient is gamma_n.
    sL0, sL1, rho_prev = sp.symbols("sL0 sL1 rho_prev")
    Slog = sp.Matrix([sL0, sL1])
    log_projection = simp((l_n.T * (Slog + rho_prev * adjacent * r_prev))[0])
    rho_solution = simp(-((l_n.T * Slog)[0]) / gamma)
    if simp(log_projection.subs(rho_prev, rho_solution)) != 0:
        raise AssertionError("log compatibility is not uniquely removable by previous kernel amplitude")

    log_source_compatible = matrix_simp(
        (Slog + rho_prev * adjacent * r_prev).subs(rho_prev, rho_solution)
    )
    log_particular = sp.Matrix([0, simp(-log_source_compatible[1] / kappa)])
    if not base._is_zero_matrix(matrix_simp(A * log_particular + log_source_compatible)):
        raise AssertionError("log compatible source lost exact range solution")

    # The current log coefficient is log_particular + eta_n r_n.  In the
    # ordinary equation eta_n cannot affect compatibility because
    # l_n^T B0'(p_n) r_n=0.  The remaining previous ordinary-kernel amplitude
    # sigma_{n-1} is therefore determined uniquely by the same gamma_n.
    sO0, sO1, sigma_prev, eta = sp.symbols("sO0 sO1 sigma_prev eta")
    Sord = sp.Matrix([sO0, sO1])
    ordinary_source = matrix_simp(
        Sord + sigma_prev * adjacent * r_prev + D * (log_particular + eta * r_n)
    )
    ordinary_projection = simp((l_n.T * ordinary_source)[0])
    ordinary_projection_eta = simp(sp.diff(ordinary_projection, eta))
    if ordinary_projection_eta != 0:
        raise AssertionError("ordinary compatibility depends on current log-kernel freedom")

    ordinary_at_sigma0 = simp(ordinary_projection.subs(sigma_prev, 0))
    sigma_solution = simp(-ordinary_at_sigma0 / gamma)
    if simp(ordinary_projection.subs(sigma_prev, sigma_solution)) != 0:
        raise AssertionError("ordinary compatibility is not uniquely removable by previous kernel amplitude")

    ordinary_source_compatible = matrix_simp(
        ordinary_source.subs(sigma_prev, sigma_solution)
    )
    ordinary_particular = sp.Matrix(
        [0, simp(-ordinary_source_compatible[1] / kappa)]
    )
    if not base._is_zero_matrix(
        matrix_simp(A * ordinary_particular + ordinary_source_compatible)
    ):
        raise AssertionError("ordinary compatible source lost exact range solution")

    # The two newly solved coefficients retain fresh right-kernel freedoms.
    # Those freedoms are precisely the two scalar variables fixed at the next
    # order by the same mechanism.  This is the induction closure for every
    # n>=3 with kappa_n !=0 and gamma_n !=0.
    compatibility_det = simp(gamma**2)

    print("GFE_CORRECTED_FINITE_BETA_EXCEPTIONAL_ALL_ORDER_FORMAL_RECURRENCE")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/(4*M); alpha=1/2")
    print("LEADING_BLOCK_FACTORIZATION := A_n=kappa_n*c_n*d_n^T")
    print("KAPPA_N := " + sp.sstr(kappa))
    print("RIGHT_KERNEL_R_N := [1, 2*M*(2*n+1)]")
    print("LEFT_PROJECTOR_L_N := [1, 2*M*(2*n-3)]")
    print("ADJACENT_KERNEL_COUPLING_GAMMA_N := " + sp.sstr(gamma))
    print("COMPATIBILITY_DETERMINANT := " + sp.sstr(compatibility_det))
    print("DISCRETE_RESONANCE_BETA_N := " + sp.sstr(beta_n) + " for integer n>=3")
    print("LOG_KERNEL_DECOUPLING := 0")
    print("LOG_COMPATIBILITY_STEP := previous log-kernel amplitude uniquely solved when gamma_n!=0")
    print("ORDINARY_COMPATIBILITY_STEP := previous ordinary-kernel amplitude uniquely solved when gamma_n!=0")
    print("RANGE_SOLVER := exact for every source satisfying l_n^T*S=0 when kappa_n!=0")
    print("FORMAL_NONRESONANT_INDUCTION := closed for every integer n>=3")
    print("FORMAL_EXCEPTIONAL_LOG_FROBENIUS := all-order formally solvable off the discrete beta_n resonance set")
    print("GUARDS := M*beta*(5*M^2+beta)!=0 and beta!=beta_n for every integer n>=3")
    print("BOUNDARY := no convergence claim; beta=beta_n resonance surfaces remain open; no horizon-to-r_c propagation claimed")
    print("NEXT_ROUTE := analyze the discrete beta_n resonance surfaces before any global connection claim")


if __name__ == "__main__":
    main()
