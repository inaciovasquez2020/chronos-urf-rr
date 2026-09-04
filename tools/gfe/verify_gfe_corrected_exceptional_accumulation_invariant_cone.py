#!/usr/bin/env python3
"""Certify an exact invariant growth cone for the physical accumulation branch.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.
The finite-lag transfer is re-derived from the corrected Euler artifact.

Cone for n>=60:
  a_n := (-1)^(n+1) kappa_n > 0,
  2 <= a_n/(n^2 a_{n-1}) <= 5,
  |xi_n| <= a_n/n^3.

The two-sided ratio cone places the physical top-log coefficient vector between
fixed exponential multiples of (n!)^2.  Hence, under the standard formal-series
convention |c_n| <= C A^n (n!)^s, its exact minimal Gevrey exponent is 2.
Every tail inequality is reduced to positivity of a shifted exact rational
polynomial; no floating-point inequalities are used.
"""
from __future__ import annotations

import sympy as sp
import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def ms(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


def shifted_nonnegative(poly_expr: sp.Expr, n: sp.Symbol, N: int) -> bool:
    m = sp.symbols("m", nonnegative=True)
    poly = sp.Poly(sp.expand(poly_expr.subs(n, m + N)), m, domain=sp.QQ)
    return all(c >= 0 for c in poly.all_coeffs())


def assert_tail_nonnegative(expr: sp.Expr, n: sp.Symbol, N: int, label: str) -> None:
    expr = sp.cancel(sp.together(expr))
    num, den = sp.fraction(expr)
    if not shifted_nonnegative(num, n, N):
        raise AssertionError(label + " numerator is not coefficientwise nonnegative after tail shift")
    if not shifted_nonnegative(den, n, N):
        raise AssertionError(label + " denominator is not coefficientwise nonnegative after tail shift")


def tail_abs(expr: sp.Expr, n: sp.Symbol, N: int, label: str) -> sp.Expr:
    expr = simp(expr)
    try:
        assert_tail_nonnegative(expr, n, N, label + " positive")
        return expr
    except AssertionError:
        assert_tail_nonnegative(-expr, n, N, label + " negative")
        return simp(-expr)


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
        q = equation.xreplace(trial).subs({
            base.r: 2 + x,
            base.M: 1,
            base.omega: base.I / 4,
            base.lam: 6,
            base.beta: sp.Rational(5, 2),
        })
        specialized.append(simp(q))
    q0, q1 = specialized

    F = ms(sp.Matrix([
        [sp.diff(simp(x**3*q0), a), sp.diff(simp(x**3*q0), b)],
        [sp.diff(simp(x**2*q1), a), sp.diff(simp(x**2*q1), b)],
    ]))
    Dp = sp.Poly(1, x, domain="EX")
    for entry in F:
        _, den = sp.fraction(simp(entry))
        Dp = sp.lcm(Dp, sp.Poly(den, x, domain="EX").monic())
    D = simp(Dp.as_expr() / Dp.as_expr().subs(x, 0))
    C = ms(D * F)
    J = max(sp.Poly(entry, x, domain="EX").degree() for entry in C if entry != 0)
    Cj = [ms(sp.Matrix([
        [sp.Poly(C[row,col], x, domain="EX").coeff_monomial(x**j) for col in range(2)]
        for row in range(2)
    ])) for j in range(J+1)]
    if J != 10:
        raise AssertionError(f"finite lag changed: {J}")

    alpha = sp.Rational(1,2)
    A = ms(Cj[0].subs(p, alpha+n))
    A00 = simp(A[0,0])
    E = sp.Matrix([1,0])
    rvec = lambda k: sp.Matrix([1, 2*(2*k+1)])
    lvec = lambda k: sp.Matrix([1, 2*(2*k-3)])

    X_xi, X_kap = {}, {}
    for j in range(1,J+1):
        block = ms(Cj[j].subs(p, alpha+n-j))
        X_xi[j] = simp(-block[0,0]/A00)
        X_kap[j] = simp(-((sp.Matrix([[block[0,0],block[0,1]]])*rvec(n-j))[0])/A00)

    ell_next = lvec(n+1)
    C1n = ms(Cj[1].subs(p, alpha+n))
    gamma = simp((ell_next.T*C1n*rvec(n))[0])
    if simp(gamma + sp.Rational(125,6)*n**2) != 0:
        raise AssertionError("accumulation gamma changed")
    cxi = simp((ell_next.T*C1n*E)[0])
    K_xi = {j:simp(-cxi*X_xi[j]/gamma) for j in range(1,J+1)}
    K_kap = {j:simp(-cxi*X_kap[j]/gamma) for j in range(1,J+1)}
    for j in range(2,J+1):
        lag=j-1
        block=ms(Cj[j].subs(p, alpha+n+1-j))
        K_xi[lag]=simp(K_xi.get(lag,0)-(ell_next.T*block*E)[0]/gamma)
        K_kap[lag]=simp(K_kap.get(lag,0)-(ell_next.T*block*rvec(n+1-j))[0]/gamma)

    xi = {0:sp.Rational(0), 1:sp.Rational(20,27)}
    kap = {0:sp.Rational(0), 1:sp.Rational(-5,27)}
    def val(tab, k):
        return sp.Rational(0) if k < 0 else tab.get(k, sp.Rational(0))
    def ev(expr, k):
        out=sp.cancel(expr.subs(n,k))
        if out.free_symbols:
            raise AssertionError("symbolic parameter survived unit-mass specialization")
        return sp.Rational(out)
    for k in range(2,61):
        xv=sp.Rational(0); kv=sp.Rational(0)
        for j in range(1,J+1):
            xv += ev(X_xi.get(j,0),k)*val(xi,k-j)+ev(X_kap.get(j,0),k)*val(kap,k-j)
            kv += ev(K_xi.get(j,0),k)*val(xi,k-j)+ev(K_kap.get(j,0),k)*val(kap,k-j)
        xi[k]=sp.cancel(xv); kap[k]=sp.cancel(kv)

    q = sp.Rational(2)
    Q = sp.Rational(5)
    Ccone = sp.Rational(1)
    for k in range(51,61):
        ak = (-1)**(k+1) * kap[k]
        if ak <= 0:
            raise AssertionError(f"physical prefix misses kernel sign cone at n={k}")
        if k >= 52:
            ap = (-1)**k * kap[k-1]
            rr = sp.cancel(ak/(k**2*ap))
            if not (q <= rr <= Q):
                raise AssertionError(f"physical prefix misses ratio cone at n={k}: {rr}")
        if sp.cancel(abs(xi[k])*k**3-ak) > 0:
            raise AssertionError(f"physical prefix misses absolute range cone at n={k}")

    N = 61
    def hist_upper(j: int) -> sp.Expr:
        if j == 1:
            return sp.Integer(1)
        prod = sp.Integer(1)
        for s in range(1,j):
            prod *= (n-s)**2
        return simp(1/(q**(j-1)*prod))

    absKxi={j:tail_abs(K_xi.get(j,0),n,N,f"Kxi{j}") for j in range(1,J+1)}
    absKkap={j:tail_abs(K_kap.get(j,0),n,N,f"Kkap{j}") for j in range(1,J+1)}
    absXxi={j:tail_abs(X_xi.get(j,0),n,N,f"Xxi{j}") for j in range(1,J+1)}
    absXkap={j:tail_abs(X_kap.get(j,0),n,N,f"Xkap{j}") for j in range(1,J+1)}

    kernel_dom = simp(-K_kap[1]/n**2)
    assert_tail_nonnegative(kernel_dom,n,N,"kernel dominant coefficient")
    kernel_rem = sp.Integer(0)
    for j in range(1,J+1):
        hu=hist_upper(j)
        kernel_rem += absKxi[j]*hu/((n-j)**3*n**2)
        if j >= 2:
            kernel_rem += absKkap[j]*hu/n**2
    kernel_rem=simp(kernel_rem)
    assert_tail_nonnegative(kernel_dom-kernel_rem-q,n,N,"kernel lower cone")
    assert_tail_nonnegative(Q-kernel_dom-kernel_rem,n,N,"kernel upper cone")

    # Absolute range bound; no sign assumption on xi is needed.
    range_abs = sp.Integer(0)
    for j in range(1,J+1):
        hu=hist_upper(j)
        range_abs += absXkap[j]*hu + absXxi[j]*hu/(n-j)**3
    range_abs=simp(range_abs)
    # a_n >= q*n^2*a_{n-1}; therefore this sufficient inequality preserves
    # |xi_n| <= a_n/n^3.
    assert_tail_nonnegative(Ccone*q/n-range_abs,n,N,"absolute range magnitude cone")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_INVARIANT_CONE_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("TAIL_START := 61")
    print("KERNEL_SIGN := (-1)^(n+1)*kappa_n > 0")
    print("FACTORIAL_RATIO_CONE := 2 <= (-1)^(n+1)*kappa_n/(n^2*(-1)^n*kappa_(n-1)) <= 5")
    print("RANGE_KERNEL_CONE := abs(xi_n/kappa_n) <= 1/n^3")
    print("PREFIX_CERTIFIED := full lag history 51<=n<=60 lies in kernel/range cone")
    print("TAIL_INVARIANCE := exact rational inequalities certified for every integer n>=61")
    print("FACTORIAL_LOWER_BOUND := abs(kappa_n) >= abs(kappa_60)*2^(n-60)*(n!/60!)^2 for n>=60")
    print("FACTORIAL_UPPER_BOUND := abs(kappa_n) <= abs(kappa_60)*5^(n-60)*(n!/60!)^2 for n>=60")
    print("TOP_LOG_VECTOR_GEVREY_DEFINITION := |c_n| <= C*A^n*(n!)^s")
    print("TOP_LOG_VECTOR_GEVREY_2 := certified")
    print("TOP_LOG_VECTOR_NOT_GEVREY_S_LT_2 := certified from the factorial lower bound")
    print("TOP_LOG_VECTOR_MINIMAL_GEVREY_EXPONENT := 2")
    print("PHYSICAL_FACTORIAL_SECTOR := nonzero")
    print("TOP_LOG_POWER_SERIES_RADIUS := 0")
    print("ACCUMULATION_POINT_CONVERGENT_FROBENIUS := ruled out for the physical top-log branch")
    print("BOUNDARY := accumulation coupling only; no Borel summability claim; generic beta convergence not classified; no horizon-to-r_c map; no C_phys; no global Chronos closure")


if __name__ == "__main__":
    main()
