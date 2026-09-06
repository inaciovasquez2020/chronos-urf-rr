#!/usr/bin/env python3
"""Expose exact transfer coefficients needed for an accumulation-point invariant cone.

This is a bounded diagnostic for the corrected exceptional sector
M=1, beta=5/2, omega=i/4, ell=2, lambda=6.  It re-derives the same
finite-lag transfer from the exact Euler artifact and prints only the dominant
lag-1/lag-2 kernel and range couplings needed to choose rigorous cone bounds.
"""
from __future__ import annotations

import sympy as sp
import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def ms(A: sp.Matrix) -> sp.Matrix:
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
    cxi = simp((ell_next.T*C1n*E)[0])
    K_xi = {j:simp(-cxi*X_xi[j]/gamma) for j in range(1,J+1)}
    K_kap = {j:simp(-cxi*X_kap[j]/gamma) for j in range(1,J+1)}
    for j in range(2,J+1):
        lag=j-1
        block=ms(Cj[j].subs(p, alpha+n+1-j))
        K_xi[lag]=simp(K_xi.get(lag,0)-(ell_next.T*block*E)[0]/gamma)
        K_kap[lag]=simp(K_kap.get(lag,0)-(ell_next.T*block*rvec(n+1-j))[0]/gamma)

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_CONE_COEFFICIENTS")
    print("FINITE_LAG :=", J)
    for j in (1,2,3):
        print(f"X_XI_{j} := {sp.sstr(X_xi[j])}")
        print(f"X_KAPPA_{j} := {sp.sstr(X_kap[j])}")
        print(f"K_XI_{j} := {sp.sstr(K_xi[j])}")
        print(f"K_KAPPA_{j} := {sp.sstr(K_kap[j])}")
    print("NEXT_ROUTE := certify invariant alternating-growth cone from these exact rational transfers")


if __name__ == "__main__":
    main()
