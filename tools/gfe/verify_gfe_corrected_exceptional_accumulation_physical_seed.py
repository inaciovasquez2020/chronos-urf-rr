#!/usr/bin/env python3
"""Propagate the exact physical top-log seed at the accumulation coupling.

Scope: corrected AEH=1/2 Euler system, ell=2, lambda=6,
omega=i/(4M), beta=5 M^2/2.  We use the dimensionless unit-mass
normalization M=1 and derive the finite-lag recurrence directly from the exact
Euler artifact.  This is a finite-prefix diagnostic only: it tests whether the
physical top-log sequence exhibits the slope-two factorial signature found by
the Newton audit and exposes the tail contribution pattern needed for a
rigorous invariant-cone proof.  It does not by itself prove the asymptotic
sector amplitude.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def matrix_simp(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


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
        raise AssertionError("unit-mass analytic denominator lost horizon normalization")

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
        raise AssertionError("unit-mass accumulation coupling changed")

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

    N = 60
    for k in range(2, N + 1):
        xi_k = sp.Rational(0)
        kap_k = sp.Rational(0)
        for j in range(1, J + 1):
            xi_k += eval_at(X_xi.get(j, 0), k) * value(xi, k - j)
            xi_k += eval_at(X_kap.get(j, 0), k) * value(kap, k - j)
            kap_k += eval_at(K_xi.get(j, 0), k) * value(xi, k - j)
            kap_k += eval_at(K_kap.get(j, 0), k) * value(kap, k - j)
        xi[k] = sp.cancel(xi_k)
        kap[k] = sp.cancel(kap_k)

    expected_xi2 = sp.Rational(1412, 2025)
    if xi[2] != expected_xi2:
        raise AssertionError(
            "physical seed propagation disagrees with exact n=2 logarithmic particular: "
            f"xi2={xi[2]}"
        )

    if any(kap[k] == 0 for k in range(2, N + 1)):
        raise AssertionError("physical top-log kernel coordinate vanished in the audited prefix")

    factorial_base = sp.Rational(-18, 5)
    checkpoints = [8, 12, 20, 30, 40, 50, 60]
    ratios: dict[int, sp.Expr] = {}
    amplitudes: dict[int, sp.Expr] = {}
    range_kernel: dict[int, sp.Expr] = {}
    for k in checkpoints:
        ratios[k] = sp.cancel(kap[k] / (k**2 * kap[k - 1]))
        amplitudes[k] = sp.cancel(
            kap[k] * k**2 / (factorial_base**k * sp.factorial(k) ** 2)
        )
        range_kernel[k] = sp.cancel(xi[k] / kap[k])

    tail_k = N
    kernel_contributions: list[tuple[int, sp.Expr, sp.Expr]] = []
    for j in range(1, J + 1):
        from_xi = sp.cancel(
            eval_at(K_xi.get(j, 0), tail_k) * value(xi, tail_k - j) / kap[tail_k]
        )
        from_kap = sp.cancel(
            eval_at(K_kap.get(j, 0), tail_k) * value(kap, tail_k - j) / kap[tail_k]
        )
        kernel_contributions.append((j, from_xi, from_kap))
    contribution_sum = sp.cancel(
        sum(from_xi + from_kap for _, from_xi, from_kap in kernel_contributions)
    )
    if contribution_sum != 1:
        raise AssertionError("kernel contribution decomposition no longer sums exactly to one")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_PHYSICAL_SEED_PREFIX")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/4; M=1; beta=5/2; alpha=1/2")
    print("FINITE_LAG := " + str(J))
    print("PHYSICAL_TOP_LOG_V1 := [5/9, -10/9]")
    print("PHYSICAL_TOP_LOG_COORDINATES_N1 := xi=20/27; kappa=-5/27")
    print("PHYSICAL_TOP_LOG_XI_N2 := " + sp.sstr(xi[2]))
    print("EXPECTED_XI_N2 := 1412/2025")
    print("SLOPE2_FORMAL_FACTORIAL_BASE := -18/5")
    print("TESTED_FACTORIAL_POWER := n^(-2)")
    for k in checkpoints:
        print("SCALED_KERNEL_RATIO_N_" + str(k) + " := " + sp.sstr(sp.N(ratios[k], 24)))
        print(
            "SCALED_KERNEL_RATIO_ERROR_N_"
            + str(k)
            + " := "
            + sp.sstr(sp.N(ratios[k] - factorial_base, 24))
        )
        print(
            "FACTORIAL_NORMALIZED_AMPLITUDE_N_"
            + str(k)
            + " := "
            + sp.sstr(sp.N(amplitudes[k], 24))
        )
        print(
            "RANGE_TO_KERNEL_RATIO_N_"
            + str(k)
            + " := "
            + sp.sstr(sp.N(range_kernel[k], 24))
        )
    for j, from_xi, from_kap in kernel_contributions:
        print(
            "KERNEL_TAIL_FRACTIONS_N_60_LAG_"
            + str(j)
            + " := from_xi "
            + sp.sstr(sp.N(from_xi, 24))
            + "; from_kappa "
            + sp.sstr(sp.N(from_kap, 24))
        )
    print("KERNEL_TAIL_FRACTION_SUM_N_60 := 1")
    print("PREFIX_NONVANISHING := kappa_n != 0 for 2<=n<=60")
    print("FINITE_PREFIX_ONLY := True")
    print("FACTORIAL_SECTOR_AMPLITUDE := not yet proved from finite-prefix data")
    print("NEXT_ROUTE := use the exact tail fractions to choose and certify an invariant alternating-growth cone")


if __name__ == "__main__":
    main()
