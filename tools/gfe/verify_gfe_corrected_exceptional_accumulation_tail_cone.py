#!/usr/bin/env python3
"""Certify a factorial-growth tail cone for the physical exceptional top-log branch.

Sector: corrected AEH=1/2, ell=2, lambda=6, omega=i/(4M),
beta=5 M^2/2, with the dimensionless normalization M=1.

The exact finite-lag transfer is re-derived from the Euler artifact.  For the
physical top-log seed we certify a finite base window and then prove, by exact
rational tail inequalities, the invariant cone

    u_n := (-1)^n kappa_n > 0,
    u_n >= 3 n^2 u_(n-1),
    |xi_n| <= u_n / (3 n^3).

The first inequality implies superfactorial coefficient growth and therefore
zero radius of convergence for the top-log power-series coefficient sequence
at beta=5 M^2/2.  This is a parameter-specific negative convergence result;
it is not a global Chronos closure claim.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def matrix_simp(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


def shifted_poly_sign(poly: sp.Poly, var: sp.Symbol, start: int) -> int:
    m = sp.symbols("m", nonnegative=True)
    shifted = sp.Poly(sp.expand(poly.as_expr().subs(var, m + start)), m, domain=sp.QQ)
    coeffs = shifted.all_coeffs()
    if all(c >= 0 for c in coeffs) and any(c > 0 for c in coeffs):
        return 1
    if all(c <= 0 for c in coeffs) and any(c < 0 for c in coeffs):
        return -1
    raise AssertionError(
        "tail sign not coefficientwise certified after shift "
        + str(start)
        + ": "
        + sp.sstr(shifted.as_expr())
    )


def rational_tail_sign(expr: sp.Expr, n: sp.Symbol, start: int) -> int:
    expr = sp.cancel(sp.together(expr))
    if expr == 0:
        return 0
    num, den = sp.fraction(expr)
    num_poly = sp.Poly(num, n, domain=sp.QQ)
    den_poly = sp.Poly(den, n, domain=sp.QQ)
    return shifted_poly_sign(num_poly, n, start) * shifted_poly_sign(den_poly, n, start)


def assert_tail_nonnegative(expr: sp.Expr, n: sp.Symbol, start: int, label: str) -> None:
    expr = sp.cancel(sp.together(expr))
    if expr == 0:
        return
    sign = rational_tail_sign(expr, n, start)
    if sign != 1:
        raise AssertionError(label + " is not certified nonnegative on the tail")


def main() -> None:
    equations, h = base._parse_equations()
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
        q = q.subs(
            {
                base.r: 2 + x,
                base.M: 1,
                base.omega: base.I / 4,
                base.lam: 6,
                base.beta: sp.Rational(5, 2),
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
    D = simp(Dpoly.as_expr())
    D = simp(D / D.subs(x, 0))
    if simp(D.subs(x, 0) - 1) != 0:
        raise AssertionError("analytic denominator lost horizon normalization")

    C = matrix_simp(D * F)
    J = max(sp.Poly(entry, x, domain="EX").degree() for entry in C if entry != 0)
    Cj: list[sp.Matrix] = []
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

    alpha = sp.Rational(1, 2)
    A = matrix_simp(Cj[0].subs(p, alpha + n))
    A00 = simp(A[0, 0])
    E = sp.Matrix([1, 0])

    def rvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * (2 * k + 1)])

    def lvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * (2 * k - 3)])

    X_xi: dict[int, sp.Expr] = {}
    X_kap: dict[int, sp.Expr] = {}
    for j in range(1, J + 1):
        block = matrix_simp(Cj[j].subs(p, alpha + n - j))
        X_xi[j] = simp(-block[0, 0] / A00)
        X_kap[j] = simp(-((sp.Matrix([[block[0, 0], block[0, 1]]]) * rvec(n - j))[0]) / A00)

    ell_next = lvec(n + 1)
    C1n = matrix_simp(Cj[1].subs(p, alpha + n))
    gamma_next = simp((ell_next.T * C1n * rvec(n))[0])
    if simp(gamma_next + sp.Rational(125, 6) * n**2) != 0:
        raise AssertionError("accumulation coupling changed")

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

    # Exact physical top-log prefix, used only to seed the invariant tail cone.
    xi: dict[int, sp.Rational] = {0: sp.Rational(0), 1: sp.Rational(20, 27)}
    kap: dict[int, sp.Rational] = {0: sp.Rational(0), 1: sp.Rational(-5, 27)}

    def value(table: dict[int, sp.Rational], idx: int) -> sp.Rational:
        if idx < 0:
            return sp.Rational(0)
        return table.get(idx, sp.Rational(0))

    def eval_at(expr: sp.Expr, k: int) -> sp.Rational:
        out = sp.cancel(expr.subs(n, k))
        if out.free_symbols:
            raise AssertionError("unit-mass transfer retained symbolic parameters")
        return sp.Rational(out)

    base_end = 100
    for k in range(2, base_end + 1):
        xi_k = sp.Rational(0)
        kap_k = sp.Rational(0)
        for j in range(1, J + 1):
            xi_k += eval_at(X_xi.get(j, 0), k) * value(xi, k - j)
            xi_k += eval_at(X_kap.get(j, 0), k) * value(kap, k - j)
            kap_k += eval_at(K_xi.get(j, 0), k) * value(xi, k - j)
            kap_k += eval_at(K_kap.get(j, 0), k) * value(kap, k - j)
        xi[k] = sp.cancel(xi_k)
        kap[k] = sp.cancel(kap_k)

    growth_c = sp.Rational(3)
    range_c = sp.Rational(1, 3)
    tail_start = 101
    base_start = tail_start - J

    # Seed the ten-step recurrence window exactly.
    for k in range(base_start, tail_start):
        u_k = (-1) ** k * kap[k]
        u_prev = (-1) ** (k - 1) * kap[k - 1]
        if not (u_k > 0):
            raise AssertionError(f"alternating kernel sign fails in base window at n={k}")
        if not (u_k >= growth_c * k**2 * u_prev):
            raise AssertionError(f"factorial growth cone fails in base window at n={k}")
        if not (abs(xi[k]) <= range_c * u_k / k**3):
            raise AssertionError(f"range/kernel cone fails in base window at n={k}")

    # Sign-normalized recurrence coefficients:
    # u_n=(-1)^n kappa_n and v_n=(-1)^(n+1) xi_n.
    Acoef = {j: simp((-1) ** j * K_kap.get(j, 0)) for j in range(1, J + 1)}
    Bcoef = {j: simp((-1) ** (j + 1) * K_xi.get(j, 0)) for j in range(1, J + 1)}
    Ccoef = {j: simp((-1) ** j * X_xi.get(j, 0)) for j in range(1, J + 1)}
    Dcoef = {j: simp((-1) ** (j + 1) * X_kap.get(j, 0)) for j in range(1, J + 1)}

    absA: dict[int, sp.Expr] = {}
    absB: dict[int, sp.Expr] = {}
    absC: dict[int, sp.Expr] = {}
    absD: dict[int, sp.Expr] = {}
    for name, source, target in [
        ("A", Acoef, absA),
        ("B", Bcoef, absB),
        ("C", Ccoef, absC),
        ("D", Dcoef, absD),
    ]:
        for j in range(1, J + 1):
            expr = source[j]
            if expr == 0:
                target[j] = sp.Integer(0)
                continue
            sign = rational_tail_sign(expr, n, tail_start)
            target[j] = simp(sign * expr)
            assert_tail_nonnegative(target[j], n, tail_start, f"abs{name}_{j}")

    assert_tail_nonnegative(Acoef[1], n, tail_start, "main alternating kernel coefficient")

    # If u_m >= c m^2 u_(m-1), then for j>=1
    # u_(n-j)/u_(n-1) <= R_j, with R_1=1.
    R: dict[int, sp.Expr] = {1: sp.Integer(1)}
    for j in range(2, J + 1):
        bound = sp.Integer(1)
        for s in range(1, j):
            bound /= growth_c * (n - s) ** 2
        R[j] = simp(bound)

    # Worst-case lower bound for u_n/u_(n-1).  The main j=1 kernel term is
    # kept with its sign; every other kernel and range term is subtracted in
    # absolute value.  This deliberately sacrifices sharp cancellation.
    lower = Acoef[1]
    for j in range(2, J + 1):
        lower -= absA[j] * R[j]
    for j in range(1, J + 1):
        lower -= absB[j] * range_c * R[j] / (n - j) ** 3
    lower = simp(lower)
    growth_margin = simp(lower - growth_c * n**2)
    assert_tail_nonnegative(growth_margin, n, tail_start, "factorial growth margin")

    # Absolute range-coordinate update.  By the induction cone and the same
    # R_j bounds, |v_n|/u_(n-1) is bounded by range_upper.  Since the kernel
    # lower bound gives u_n >= c n^2 u_(n-1), it suffices to prove
    # range_upper <= range_c*c/n.
    range_upper = sp.Integer(0)
    for j in range(1, J + 1):
        range_upper += absC[j] * range_c * R[j] / (n - j) ** 3
        range_upper += absD[j] * R[j]
    range_upper = simp(range_upper)
    range_margin = simp(range_c * growth_c / n - range_upper)
    assert_tail_nonnegative(range_margin, n, tail_start, "range/kernel cone margin")

    # The cone therefore propagates for every n>=tail_start.  In particular,
    # u_n >= u_(tail_start-1) * 3^(n-tail_start+1) * (n!/(tail_start-1)!)^2,
    # so limsup |kappa_n|^(1/n)=infinity and the coefficient power series has
    # radius zero.
    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_FACTORIAL_TAIL_CONE_CERTIFIED")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/4; M=1; beta=5/2; alpha=1/2")
    print("FINITE_LAG := " + str(J))
    print("TAIL_START := " + str(tail_start))
    print("BASE_WINDOW := " + str(base_start) + ".." + str(tail_start - 1))
    print("ALTERNATING_KERNEL_COORDINATE := u_n=(-1)^n*kappa_n")
    print("INVARIANT_GROWTH := u_n >= 3*n^2*u_(n-1) > 0")
    print("INVARIANT_RANGE_CONE := |xi_n| <= u_n/(3*n^3)")
    print("GROWTH_MARGIN := exact rational function coefficientwise nonnegative after n=101 shift")
    print("RANGE_MARGIN := exact rational function coefficientwise nonnegative after n=101 shift")
    print("FACTORIAL_LOWER_BOUND := u_n grows at least like 3^n*(n!)^2 up to a fixed prefactor")
    print("TOP_LOG_COEFFICIENT_RADIUS := 0")
    print("ACCUMULATION_POINT_CONVERGENCE := closed negatively for the physical top-log Frobenius series")
    print("BOUNDARY := parameter-specific beta=5*M^2/2 result; no Borel summability claim; no horizon-to-r_c map; no C_phys; no global Chronos closure")
    print("NEXT_ROUTE := decide whether the divergent formal horizon branch admits a canonical resummation or whether the horizon variable/field basis must be changed")


if __name__ == "__main__":
    main()
