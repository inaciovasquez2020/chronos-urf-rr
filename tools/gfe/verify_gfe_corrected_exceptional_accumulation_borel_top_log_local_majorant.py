#!/usr/bin/env python3
"""Certify an explicit local majorant for the physical top-log Borel germ.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The merged invariant-cone certificate gives, for n>=61,

    a_n := (-1)^(n+1) kappa_n > 0,
    a_n/(n^2 a_(n-1)) <= 5,
    |xi_n/kappa_n| <= 1/n^3.

For the order-2 Borel coefficients

    Xi_n = xi_n/(n!)^2,   K_n = kappa_n/(n!)^2,

this implies

    |K_n| <= |K_60| 5^(n-60),
    |Xi_n| <= |K_n|/n^3.

At z*=1/10 the geometric factor is 5 z*=1/2.  Recomputing the exact
physical prefix through n=60 therefore gives rigorous uniform bounds on
Xi, K and their first three Euler jets theta^j on the whole interval
0<=z<=1/10.  These are the local quantitative inputs needed to bound the
top-log part of the two-fold Laplace reconstruction before finite-radius
physical-state propagation.

This verifier does not yet bound the ordinary Borel companion, evaluate the
double-Laplace integral, propagate the six-state physical solution to r=4096,
or claim C_grow != 0.
"""
from __future__ import annotations

import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_invariant_cone as cone
import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def physical_prefix() -> tuple[dict[int, sp.Rational], dict[int, sp.Rational]]:
    """Recompute the exact physical recurrence coordinates through n=60."""
    equations, h = base._parse_equations()
    p = base.p
    x = sp.symbols("x", positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    a, b = sp.symbols("a b")

    trial: dict[sp.Expr, sp.Expr] = {}
    for order in range(5):
        trial[h[0][order]] = a * base._falling(p, order) / x**order
        trial[h[1][order]] = b * base._falling(p - 1, order) / x ** (order + 1)

    specialized: list[sp.Expr] = []
    for equation in equations:
        value = equation.xreplace(trial).subs({
            base.r: 2 + x,
            base.M: 1,
            base.omega: base.I / 4,
            base.lam: 6,
            base.beta: sp.Rational(5, 2),
        })
        specialized.append(simp(value))
    q0, q1 = specialized

    F = ms(sp.Matrix([
        [sp.diff(simp(x**3 * q0), a), sp.diff(simp(x**3 * q0), b)],
        [sp.diff(simp(x**2 * q1), a), sp.diff(simp(x**2 * q1), b)],
    ]))

    Dpoly = sp.Poly(1, x, domain="EX")
    for entry in F:
        _, den = sp.fraction(simp(entry))
        Dpoly = sp.lcm(Dpoly, sp.Poly(den, x, domain="EX").monic())
    D = simp(Dpoly.as_expr() / Dpoly.as_expr().subs(x, 0))
    C = ms(D * F)
    J = max(sp.Poly(entry, x, domain="EX").degree() for entry in C if entry != 0)
    if J != 10:
        raise AssertionError(f"finite lag changed: {J}")

    Cj = [
        ms(sp.Matrix([
            [sp.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j) for col in range(2)]
            for row in range(2)
        ]))
        for j in range(J + 1)
    ]

    alpha = sp.Rational(1, 2)
    A = ms(Cj[0].subs(p, alpha + n))
    A00 = simp(A[0, 0])
    E = sp.Matrix([1, 0])

    def rvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * (2 * k + 1)])

    def lvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * (2 * k - 3)])

    X_xi: dict[int, sp.Expr] = {}
    X_kap: dict[int, sp.Expr] = {}
    for j in range(1, J + 1):
        block = ms(Cj[j].subs(p, alpha + n - j))
        X_xi[j] = simp(-block[0, 0] / A00)
        X_kap[j] = simp(-((sp.Matrix([[block[0, 0], block[0, 1]]]) * rvec(n - j))[0]) / A00)

    ell_next = lvec(n + 1)
    C1n = ms(Cj[1].subs(p, alpha + n))
    gamma = simp((ell_next.T * C1n * rvec(n))[0])
    if simp(gamma + sp.Rational(125, 6) * n**2) != 0:
        raise AssertionError("accumulation coupling changed")

    cxi = simp((ell_next.T * C1n * E)[0])
    K_xi = {j: simp(-cxi * X_xi[j] / gamma) for j in range(1, J + 1)}
    K_kap = {j: simp(-cxi * X_kap[j] / gamma) for j in range(1, J + 1)}
    for j in range(2, J + 1):
        lag = j - 1
        block = ms(Cj[j].subs(p, alpha + n + 1 - j))
        K_xi[lag] = simp(K_xi.get(lag, 0) - (ell_next.T * block * E)[0] / gamma)
        K_kap[lag] = simp(
            K_kap.get(lag, 0)
            - (ell_next.T * block * rvec(n + 1 - j))[0] / gamma
        )

    xi: dict[int, sp.Rational] = {0: sp.Rational(0), 1: sp.Rational(20, 27)}
    kap: dict[int, sp.Rational] = {0: sp.Rational(0), 1: sp.Rational(-5, 27)}

    def value(table: dict[int, sp.Rational], index: int) -> sp.Rational:
        if index < 0:
            return sp.Rational(0)
        return table.get(index, sp.Rational(0))

    def evaluate(expr: sp.Expr, index: int) -> sp.Rational:
        out = sp.cancel(expr.subs(n, index))
        if out.free_symbols:
            raise AssertionError("physical transfer retained symbolic parameters")
        return sp.Rational(out)

    for k in range(2, 61):
        xv = sp.Rational(0)
        kv = sp.Rational(0)
        for j in range(1, J + 1):
            xv += evaluate(X_xi.get(j, 0), k) * value(xi, k - j)
            xv += evaluate(X_kap.get(j, 0), k) * value(kap, k - j)
            kv += evaluate(K_xi.get(j, 0), k) * value(xi, k - j)
            kv += evaluate(K_kap.get(j, 0), k) * value(kap, k - j)
        xi[k] = sp.Rational(sp.cancel(xv))
        kap[k] = sp.Rational(sp.cancel(kv))

    if xi[2] != sp.Rational(1412, 2025):
        raise AssertionError("physical n=2 logarithmic anchor changed")
    if kap[60] == 0:
        raise AssertionError("physical kappa_60 vanished")
    return xi, kap


def main() -> None:
    # Re-execute the exact invariant cone rather than relying on CI ordering.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        cone.main()
    prior = buffer.getvalue()
    required = [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_INVARIANT_CONE_CERTIFIED",
        "TAIL_START := 61",
        "FACTORIAL_RATIO_CONE := 2 <= (-1)^(n+1)*kappa_n/(n^2*(-1)^n*kappa_(n-1)) <= 5",
        "RANGE_KERNEL_CONE := abs(xi_n/kappa_n) <= 1/n^3",
        "ORDER2_BOREL_TOP_LOG_RADIUS := 5/18",
    ]
    for token in required:
        if token not in prior:
            raise AssertionError("invariant-cone dependency changed: " + token)

    xi, kap = physical_prefix()
    zstar = sp.Rational(1, 10)
    q = 5 * zstar
    if q != sp.Rational(1, 2):
        raise AssertionError("chosen local Borel majorant lost geometric half-factor")

    bxi = {n: sp.Rational(xi[n], sp.factorial(n) ** 2) for n in range(61)}
    bkap = {n: sp.Rational(kap[n], sp.factorial(n) ** 2) for n in range(61)}
    K60 = abs(bkap[60])
    if K60 <= 0:
        raise AssertionError("order-2 Borel K_60 anchor is not positive in modulus")

    # Exact sums sum_{m>=1} (m+60)^j / 2^m for j=0,1,2,3.
    tail_moments = [sp.Integer(1), sp.Integer(62), sp.Integer(3846), sp.Integer(238706)]
    m = sp.symbols("m", integer=True, positive=True)
    for jet, expected in enumerate(tail_moments):
        actual = sp.summation((m + 60) ** jet * q**m, (m, 1, sp.oo))
        if sp.simplify(actual - expected) != 0:
            raise AssertionError(f"geometric jet moment changed at order {jet}: {actual}")

    xi_bounds: list[sp.Rational] = []
    kap_bounds: list[sp.Rational] = []
    xi_tail_bounds: list[sp.Rational] = []
    kap_tail_bounds: list[sp.Rational] = []

    for jet in range(4):
        prefix_xi = sum(
            abs(bxi[n]) * n**jet * zstar**n
            for n in range(1, 61)
        )
        prefix_kap = sum(
            abs(bkap[n]) * n**jet * zstar**n
            for n in range(1, 61)
        )

        # From the ratio-cone upper bound after dividing by (n!)^2:
        # |K_n| <= |K_60| 5^(n-60).  The range cone gives the Xi bound.
        tail_kap = sp.Rational(K60 * zstar**60 * tail_moments[jet])
        if jet <= 3:
            tail_xi = sp.Rational(K60 * zstar**60 / sp.Integer(61) ** (3 - jet))
        else:
            raise AssertionError("unexpected Euler-jet order")

        kap_tail_bounds.append(tail_kap)
        xi_tail_bounds.append(tail_xi)
        kap_bounds.append(sp.Rational(prefix_kap + tail_kap))
        xi_bounds.append(sp.Rational(prefix_xi + tail_xi))

        if kap_bounds[-1] <= 0 or xi_bounds[-1] <= 0:
            raise AssertionError("local top-log majorant is not positive")

    # W_L=S(theta)V_L with S=[[1,1],[0,4 theta+2]].  These two bounds are
    # enough to control the top-log physical-field pair on the local Borel box.
    W0_bound = sp.Rational(xi_bounds[0] + kap_bounds[0])
    W1_bound = sp.Rational(4 * kap_bounds[1] + 2 * kap_bounds[0])

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_TOP_LOG_LOCAL_MAJORANT_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("ORDER2_BOREL_COORDINATES := Xi_n=xi_n/(n!)^2; K_n=kappa_n/(n!)^2")
    print("LOCAL_MAJORANT_INTERVAL := 0 <= z <= 1/10")
    print("INVARIANT_TAIL_START := n >= 61")
    print("BOREL_KERNEL_TAIL_STEP := |K_n| <= |K_60|*5^(n-60)")
    print("BOREL_RANGE_TAIL_STEP := |Xi_n| <= |K_n|/n^3")
    print("GEOMETRIC_FACTOR_AT_ENDPOINT := 5*(1/10)=1/2")
    print(f"BOREL_K60_ABS := {sp.sstr(K60)}")
    for jet in range(4):
        print(f"THETA_JET_{jet}_XI_TAIL_BOUND := {sp.sstr(xi_tail_bounds[jet])}")
        print(f"THETA_JET_{jet}_K_TAIL_BOUND := {sp.sstr(kap_tail_bounds[jet])}")
        print(f"THETA_JET_{jet}_XI_UNIFORM_BOUND := {sp.sstr(xi_bounds[jet])}")
        print(f"THETA_JET_{jet}_K_UNIFORM_BOUND := {sp.sstr(kap_bounds[jet])}")
    print(f"TOP_LOG_W0_UNIFORM_BOUND := {sp.sstr(W0_bound)}")
    print(f"TOP_LOG_W1_UNIFORM_BOUND := {sp.sstr(W1_bound)}")
    print("UNIFORMITY := all bounds hold on the full real interval 0<=z<=1/10 by coefficientwise absolute majorization")
    print("NEXT_ROUTE := construct the analogous explicit ordinary-companion local majorant, then bound the two-fold Laplace startup state")
    print("BOUNDARY := top-log local Borel majorant only; ordinary companion, finite-x Laplace state, r=4096 propagation, C_grow value/nonvanishing, and global exceptional-mode closure remain unproved")


if __name__ == "__main__":
    main()
