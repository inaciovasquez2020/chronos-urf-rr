#!/usr/bin/env python3
"""Audit coefficient growth at the exceptional accumulation coupling beta=5 M^2/2.

Scope: corrected AEH=1/2 Euler system, ell=2, lambda=6,
omega=i/(4M), alpha=1/2.  This convergence diagnostic derives the finite-lag
Euler symbol directly from the exact Euler artifact, clears the analytic
x-denominator, computes the large-n transfer degrees, factors the degree-two
kernel lag polynomial, and classifies its Newton-polygon balances.

The result still does not decide whether the fixed physical logarithmic seed has
zero amplitude in the factorial sector; that is kept as the next boundary.
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


def leading_at_infinity(expr: sp.Expr, n: sp.Symbol) -> sp.Expr:
    expr = simp(expr)
    if expr == 0:
        return sp.Integer(0)
    num, den = sp.fraction(expr)
    num_poly = sp.Poly(num, n, domain="EX")
    den_poly = sp.Poly(den, n, domain="EX")
    return simp(num_poly.LC() / den_poly.LC())


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


def upper_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Upper concave hull with slopes weakly decreasing from left to right."""
    hull: list[tuple[int, int]] = []
    for point in points:
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            lhs = (y1 - y0) * (x2 - x1)
            rhs = (y2 - y1) * (x1 - x0)
            if lhs < rhs:
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


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
    z = sp.symbols("z")
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

    X_xi: dict[int, sp.Expr] = {}
    X_kap: dict[int, sp.Expr] = {}
    for j in range(1, J + 1):
        block = matrix_simp(Cj[j].subs(p, alpha + n - j))
        X_xi[j] = simp(-block[0, 0] / A00)
        X_kap[j] = simp(-((sp.Matrix([[block[0, 0], block[0, 1]]]) * rvec(n - j))[0]) / A00)

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
    kappa_degree_profile = {0: 0}
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
        if K_kap.get(j, 0) != 0:
            kappa_degree_profile[j] = row[3]

    kernel_self_degree2_coeffs: dict[int, sp.Expr] = {}
    for j in range(1, J + 1):
        expr = K_kap.get(j, 0)
        if degree_at_infinity(expr, n) == 2:
            kernel_self_degree2_coeffs[j] = leading_at_infinity(expr, n)
    kernel_self_degree2_poly = sp.factor(
        sum(coeff * z**j for j, coeff in kernel_self_degree2_coeffs.items())
    )
    expected_degree2_poly = simp(
        -3 * z * (2 * M + z) ** 2 * (12 * M**2 + 6 * M * z + z**2)
        / (40 * M**5)
    )
    if simp(kernel_self_degree2_poly - expected_degree2_poly) != 0:
        raise AssertionError("degree-two lag polynomial factorization changed")

    kernel_cross_degree1_poly = sp.factor(
        sum(
            leading_at_infinity(K_xi.get(j, 0), n) * z**j
            for j in range(1, J + 1)
            if degree_at_infinity(K_xi.get(j, 0), n) == 1
        )
    )

    # Newton polygon for the scalar kernel recurrence after eliminating the
    # range coordinate.  The current term has degree 0; lagged self-transfer
    # degrees are read exactly from K_kap.  The upper hull exposes a slope-2
    # edge of horizontal length one (the possible (n!)^2 sector), a slope-zero
    # edge of length four (four geometric sectors), and two decaying edges.
    profile_points = sorted(kappa_degree_profile.items())
    hull = upper_hull(profile_points)
    expected_hull = [(0, 0), (1, 2), (5, 2), (8, 0), (10, -2)]
    if hull != expected_hull:
        raise AssertionError(f"kernel Newton polygon changed: {hull}")
    hull_slopes = [
        sp.Rational(y1 - y0, x1 - x0)
        for (x0, y0), (x1, y1) in zip(hull, hull[1:])
    ]
    expected_slopes = [sp.Integer(2), sp.Integer(0), sp.Rational(-2, 3), sp.Integer(-1)]
    if hull_slopes != expected_slopes:
        raise AssertionError(f"kernel Newton slopes changed: {hull_slopes}")

    factorial_base = simp(kernel_self_degree2_coeffs[1])
    if simp(factorial_base + sp.Rational(18, 5) / M) != 0:
        raise AssertionError("slope-two leading factorial base changed")

    sqrt3 = sp.sqrt(3)
    nonzero_edge_roots = [
        -2 * M,
        -2 * M,
        M * (-3 + I * sqrt3),
        M * (-3 - I * sqrt3),
    ]
    edge_poly_without_zero = simp(kernel_self_degree2_poly / z)
    for root in nonzero_edge_roots:
        if simp(edge_poly_without_zero.subs(z, root)) != 0:
            raise AssertionError(f"geometric edge root changed: {sp.sstr(root)}")

    geometric_ratios = [
        simp(1 / nonzero_edge_roots[0]),
        simp(1 / nonzero_edge_roots[1]),
        simp(1 / nonzero_edge_roots[2]),
        simp(1 / nonzero_edge_roots[3]),
    ]
    expected_ratios = [
        -1 / (2 * M),
        -1 / (2 * M),
        (-3 - I * sqrt3) / (12 * M),
        (-3 + I * sqrt3) / (12 * M),
    ]
    for actual, expected in zip(geometric_ratios, expected_ratios):
        if simp(actual - expected) != 0:
            raise AssertionError("geometric ratio classification changed")

    Dpj = [matrix_simp(block.diff(p)) for block in Cj]
    max_derivative_degree = max(
        sp.Poly(entry, p, domain="EX").degree()
        for block in Dpj
        for entry in block
        if entry != 0
    )
    if max_derivative_degree > 3:
        raise AssertionError("exponent-derivative forcing degree exceeds three")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_POINT_NEWTON_AUDIT")
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
    print("KERNEL_SELF_DEGREE2_COEFFICIENTS := " + sp.sstr(kernel_self_degree2_coeffs))
    print("KERNEL_SELF_DEGREE2_LAG_POLYNOMIAL := " + sp.sstr(kernel_self_degree2_poly))
    print("KERNEL_CROSS_DEGREE1_LAG_POLYNOMIAL := " + sp.sstr(kernel_cross_degree1_poly))
    print("KERNEL_NEWTON_UPPER_HULL := " + sp.sstr(hull))
    print("KERNEL_NEWTON_SLOPES := " + sp.sstr(hull_slopes))
    print("SLOPE2_EDGE_LENGTH := 1")
    print("SLOPE2_FORMAL_FACTORIAL_BASE := " + sp.sstr(factorial_base))
    print("SLOPE0_EDGE_LENGTH := 4")
    print("SLOPE0_NONZERO_LAG_ROOTS := [" + ", ".join(sp.sstr(v) for v in nonzero_edge_roots) + "]")
    print("SLOPE0_GEOMETRIC_RATIOS := [" + ", ".join(sp.sstr(v) for v in geometric_ratios) + "]")
    print("NONLOG_EXPONENT_DERIVATIVE_MAX_P_DEGREE := " + str(max_derivative_degree))
    print("ACCUMULATION_POINT_CONVERGENCE := undecided for the fixed physical seed")
    print("BOUNDARY := one slope-2 factorial sector exists algebraically; it is not yet known whether the physical logarithmic seed excites it")
    print("NEXT_ROUTE := propagate the exact physical top-log seed and test its projection onto the slope-2 sector")


if __name__ == "__main__":
    main()
