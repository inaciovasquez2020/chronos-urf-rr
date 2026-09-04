#!/usr/bin/env python3
"""Audit coefficient growth at the exceptional accumulation coupling beta=5 M^2/2.

Scope: corrected AEH=1/2 Euler system, ell=2, lambda=6,
omega=i/(4M), alpha=1/2.  This is the first convergence diagnostic for the
all-order exceptional horizon branch.  It derives the finite-lag Euler symbol
directly from the exact Euler artifact, clears the analytic x-denominator, and
computes the large-n degree of the induced transfer coefficients.

A bounded-transfer outcome closes the standard geometric majorant.  A positive
transfer degree is reported as a precise rescaling boundary rather than being
silently promoted to convergence.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def matrix_simp(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


def degree_at_infinity(expr: sp.Expr, n: sp.Symbol) -> int:
    expr = simp(expr)
    if expr == 0:
        return -10**6
    num, den = sp.fraction(expr)
    return sp.Poly(num, n, domain="EX").degree() - sp.Poly(den, n, domain="EX").degree()


def assert_no_integer_poles(expr: sp.Expr, n: sp.Symbol) -> None:
    expr = simp(expr)
    if expr == 0:
        return
    _, den = sp.fraction(expr)
    den_poly = sp.Poly(den, n, domain="EX")
    monic = sp.factor(den_poly.monic().as_expr())
    extras = monic.free_symbols - {n}
    if extras:
        raise AssertionError(
            "n-dependent transfer denominator still depends on physical parameters: "
            + sp.sstr(monic)
        )
    qpoly = sp.Poly(monic, n, domain=sp.QQ)
    for root, _multiplicity in sp.polys.polytools.ground_roots(qpoly).items():
        if root.is_integer and root >= 3:
            raise AssertionError(f"transfer coefficient has an integer pole at n={root}")


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

    beta_acc = sp.Rational(5, 2) * M**2
    specialized = []
    for equation in equations:
        q = equation.xreplace(trial)
        q = q.subs(
            {
                r: 2 * M + x,
                omega: I / (4 * M),
                lam: 6,
                beta: beta_acc,
            }
        )
        specialized.append(simp(q))

    q0, q1 = specialized

    # Row scaling by x^3 and x^2 removes the certified horizon orders.  The
    # remaining common rational x-denominator must be analytic and nonzero at
    # x=0 before a Frobenius majorant can be discussed.
    F = matrix_simp(
        sp.Matrix(
            [
                [sp.diff(simp(x**3 * q0), a), sp.diff(simp(x**3 * q0), b)],
                [sp.diff(simp(x**2 * q1), a), sp.diff(simp(x**2 * q1), b)],
            ]
        )
    )

    den_polys = []
    for entry in F:
        _, den = sp.fraction(simp(entry))
        den_polys.append(sp.Poly(den, x, domain="EX").monic())

    Dpoly = sp.Poly(1, x, domain="EX")
    for poly in den_polys:
        Dpoly = sp.lcm(Dpoly, poly)

    D = sp.factor(Dpoly.as_expr())
    D0 = simp(D.subs(x, 0))
    if D0 == 0:
        raise AssertionError("row-scaled exceptional symbol still has a horizon pole")
    D = simp(D / D0)
    if simp(D.subs(x, 0) - 1) != 0:
        raise AssertionError("normalized analytic denominator is not one at the horizon")

    C = matrix_simp(D * F)
    entry_polys = []
    for entry in C:
        _, den = sp.fraction(entry)
        if x in den.free_symbols:
            raise AssertionError("common denominator did not clear the x dependence")
        entry_polys.append(sp.Poly(entry, x, domain="EX"))

    J = max(poly.degree() for poly in entry_polys)
    if J < 1:
        raise AssertionError("no lower-triangular lag was found")

    Cj = []
    for j in range(J + 1):
        Cj.append(
            matrix_simp(
                sp.Matrix(
                    [
                        [
                            sp.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j)
                            for col in range(2)
                        ]
                        for row in range(2)
                    ]
                )
            )
        )

    max_p_degree = max(
        sp.Poly(entry, p, domain="EX").degree()
        for block in Cj
        for entry in block
        if entry != 0
    )
    if max_p_degree > 4:
        raise AssertionError("exceptional Euler symbol has derivative degree above four")

    alpha = sp.Rational(1, 2)
    A = matrix_simp(Cj[0].subs(p, alpha + n))

    corrected_prefactor = simp(beta_acc * (5 * M**2 + beta_acc))
    kappa = simp(-corrected_prefactor * n * (n - 1) / (32 * M**5))
    c_n = sp.Matrix([-2 * M * (2 * n - 3), 1])
    d_n = sp.Matrix([-2 * M * (2 * n + 1), 1])
    if not base._is_zero_matrix(matrix_simp(A - kappa * c_n * d_n.T)):
        raise AssertionError("denominator clearing changed the certified leading block")

    E = sp.Matrix([1, 0])

    def rvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * M * (2 * k + 1)])

    def lvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * M * (2 * k - 3)])

    A00 = simp(A[0, 0])
    if A00 == 0:
        raise AssertionError("chosen rank-one complement has zero leading coefficient")

    # v_n = xi_n E + kappa_n r_n.  First-row inversion gives xi_n from the
    # finite set of lagged xi/kappa coordinates.
    X_xi: dict[int, sp.Expr] = {}
    X_kap: dict[int, sp.Expr] = {}
    for j in range(1, J + 1):
        block = matrix_simp(Cj[j].subs(p, alpha + n - j))
        X_xi[j] = simp(-block[0, 0] / A00)
        X_kap[j] = simp(-((sp.Matrix([[block[0, 0], block[0, 1]]]) * rvec(n - j))[0]) / A00)

    # The compatibility equation at order n+1 fixes the current kernel
    # coordinate kappa_n.  This is the same exact finite-lag elimination used
    # in the older repository convergence certificate, but re-derived here
    # from the corrected Euler artifact and specialized beta=5 M^2/2.
    ell_next = lvec(n + 1)
    C1n = matrix_simp(Cj[1].subs(p, alpha + n))
    gamma_next = simp((ell_next.T * C1n * rvec(n))[0])

    coupling_bracket_next = simp(
        30 * M**2 * (n + 1) * (n - 1)
        - (12 * (n + 1) * (n - 1) - 5) * beta_acc
    )
    expected_gamma_next = simp(
        -2 * beta_acc * n**2 * coupling_bracket_next / (3 * M**4)
    )
    if simp(gamma_next - expected_gamma_next) != 0:
        raise AssertionError("finite-lag compatibility coupling disagrees with formal recurrence")

    expected_accum_bracket = simp(5 * beta_acc)
    if simp(coupling_bracket_next - expected_accum_bracket) != 0:
        raise AssertionError("beta=5 M^2/2 no longer cancels the quadratic coupling growth")

    cxi = simp((ell_next.T * C1n * E)[0])
    K_xi: dict[int, sp.Expr] = {
        j: simp(-cxi * X_xi[j] / gamma_next) for j in range(1, J + 1)
    }
    K_kap: dict[int, sp.Expr] = {
        j: simp(-cxi * X_kap[j] / gamma_next) for j in range(1, J + 1)
    }

    for j in range(2, J + 1):
        lag = j - 1
        block = matrix_simp(Cj[j].subs(p, alpha + n + 1 - j))
        K_xi[lag] = simp(
            K_xi.get(lag, 0) - (ell_next.T * block * E)[0] / gamma_next
        )
        K_kap[lag] = simp(
            K_kap.get(lag, 0)
            - (ell_next.T * block * rvec(n + 1 - j))[0] / gamma_next
        )

    degree_rows = []
    max_transfer_degree = -10**6
    for j in range(1, J + 1):
        row_exprs = [
            X_xi.get(j, 0),
            X_kap.get(j, 0),
            K_xi.get(j, 0),
            K_kap.get(j, 0),
        ]
        for expr in row_exprs:
            assert_no_integer_poles(expr, n)
        row = [degree_at_infinity(expr, n) for expr in row_exprs]
        degree_rows.append((j, row))
        max_transfer_degree = max(max_transfer_degree, *row)

    Dpj = [matrix_simp(block.diff(p)) for block in Cj]
    max_derivative_degree = max(
        sp.Poly(entry, p, domain="EX").degree()
        for block in Dpj
        for entry in block
        if entry != 0
    )
    if max_derivative_degree > 3:
        raise AssertionError("exponent-derivative forcing degree exceeds three")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_POINT_GROWTH_AUDIT")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/(4*M); alpha=1/2")
    print("BETA_ACCUMULATION := 5*M**2/2")
    print("COMMON_ANALYTIC_DENOMINATOR := " + sp.sstr(D))
    print("COMMON_DENOMINATOR_AT_HORIZON := 1")
    print("FINITE_LAG := " + str(J))
    print("EULER_SYMBOL_MAX_P_DEGREE := " + str(max_p_degree))
    print("ACCUMULATION_GAMMA_N_PLUS_1 := " + sp.sstr(gamma_next))
    print("ACCUMULATION_COUPLING_BRACKET := " + sp.sstr(coupling_bracket_next))
    for lag, degrees in degree_rows:
        print(
            "LOG_TRANSFER_DEGREES_LAG_"
            + str(lag)
            + " := xi<-xi "
            + str(degrees[0])
            + "; xi<-kappa "
            + str(degrees[1])
            + "; kappa<-xi "
            + str(degrees[2])
            + "; kappa<-kappa "
            + str(degrees[3])
        )
    print("MAX_LOG_TRANSFER_DEGREE := " + str(max_transfer_degree))
    print("NONLOG_EXPONENT_DERIVATIVE_MAX_P_DEGREE := " + str(max_derivative_degree))

    if max_transfer_degree <= 0:
        print("BOUNDED_LOG_TRANSFER := certified for integer n>=3")
        print(
            "LOG_MAJORANT := finite lag + pole-free bounded transfer closes a geometric coefficient majorant"
        )
        print(
            "NONLOG_MAJORANT := polynomial exponent-derivative forcing is absorbed by an arbitrarily small enlargement of the geometric base"
        )
        print("ACCUMULATION_POINT_CONVERGENCE := certified locally on a fixed log branch")
        print("RESULT := beta=5*M**2/2 exceptional logarithmic Frobenius convergence proved")
        print(
            "BOUNDARY := no explicit optimal radius; no horizon-to-r_c continuation; no C_phys; no global Chronos closure"
        )
        print("NEXT_ROUTE := extend the transfer bound uniformly to generic beta>0 and the isolated beta_n resonance cases")
    else:
        print(
            "ACCUMULATION_POINT_CONVERGENCE := not yet closed in the unscaled kernel coordinate"
        )
        print(
            "BOUNDARY := positive polynomial transfer growth remains after analytic denominator clearing"
        )
        print(
            "NEXT_ROUTE := rescale only the kernel coordinate by n^d with d=MAX_LOG_TRANSFER_DEGREE and recompute the transfer"
        )


if __name__ == "__main__":
    main()
