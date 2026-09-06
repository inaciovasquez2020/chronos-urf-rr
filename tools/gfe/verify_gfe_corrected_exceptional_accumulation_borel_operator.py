#!/usr/bin/env python3
"""Certify the exact cleared order-2 Borel differential operator.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

Starting from the hash-locked corrected Euler artifact, reconstruct the exact
finite-lag matrix recurrence

  sum_{j=0}^J C_j(alpha+n-j) v_{n-j} = 0,  J=10,

with v_n = xi_n E + kappa_n r_n and r_n=(1,4n+2)^T.  For the order-2 Borel
coordinates Xi_n=xi_n/(n!)^2 and K_n=kappa_n/(n!)^2, define

  U(z)=(Xi(z),K(z))^T,  theta=z d/dz,
  S(theta)=[[1,1],[0,4 theta+2]],
  F_m(theta)=theta(theta-1)...(theta-m+1).

The normal-ordered cleared operator is

  B(z,theta) = sum_{j=0}^J z^j C_j(alpha+theta)
                              F_{J-j}(theta)^2 S(theta).

Because z is kept to the left of every polynomial in theta, coefficient
extraction is exact despite theta*z=z*(theta+1).  At coefficient n>=J, the
j-th term equals the corresponding original recurrence term divided by the
common factor (n-J)!^2.  The verifier checks that identity symbolically and
then checks B U=0 against the exact physical prefix n=10,...,60.

This is intentionally an unreduced annihilating operator.  Clearing the
factorial shifts introduces low-degree polynomial kernel factors; no claim is
made here that the operator is minimal, that its leading determinant gives the
genuine Borel singular set, or that analytic continuation is established.
"""
from __future__ import annotations

import sympy as sp
import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def ms(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


def is_zero_matrix(A: sp.Matrix) -> bool:
    return all(simp(entry) == 0 for entry in A)


def falling(q: sp.Expr, order: int) -> sp.Expr:
    out = sp.Integer(1)
    for s in range(order):
        out *= q - s
    return sp.expand(out)


def main() -> None:
    equations, h = base._parse_equations()
    p = base.p
    x = sp.symbols("x", positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    z, theta = sp.symbols("z theta")
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
        [sp.diff(simp(x**3 * q0), a), sp.diff(simp(x**3 * q0), b)],
        [sp.diff(simp(x**2 * q1), a), sp.diff(simp(x**2 * q1), b)],
    ]))
    Dp = sp.Poly(1, x, domain="EX")
    for entry in F:
        _, den = sp.fraction(simp(entry))
        Dp = sp.lcm(Dp, sp.Poly(den, x, domain="EX").monic())
    D = simp(Dp.as_expr() / Dp.as_expr().subs(x, 0))
    C = ms(D * F)
    J = max(sp.Poly(entry, x, domain="EX").degree() for entry in C if entry != 0)
    if J != 10:
        raise AssertionError(f"finite lag changed: {J}")

    Cj = [
        ms(sp.Matrix([
            [
                sp.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j)
                for col in range(2)
            ]
            for row in range(2)
        ]))
        for j in range(J + 1)
    ]

    alpha = sp.Rational(1, 2)
    S = sp.Matrix([[1, 1], [0, 4 * theta + 2]])

    operator_blocks = []
    B = sp.zeros(2, 2)
    for j in range(J + 1):
        block = ms(
            Cj[j].subs(p, alpha + theta)
            * falling(theta, J - j) ** 2
            * S
        )
        operator_blocks.append(block)
        B += z**j * block
    B = B.applyfunc(sp.expand)

    # Normal ordering is part of the certificate: all z powers are on the left
    # and every coefficient is a polynomial in theta.
    z_degree = 0
    theta_order = 0
    for entry in B:
        poly_z = sp.Poly(entry, z, domain="EX")
        z_degree = max(z_degree, poly_z.degree())
        for coeff in poly_z.all_coeffs():
            theta_poly = sp.Poly(sp.expand(coeff), theta, domain="EX")
            theta_order = max(theta_order, theta_poly.degree())
    if z_degree != J:
        raise AssertionError(f"cleared Borel z-degree changed: {z_degree}")

    # Check exact z^j block extraction from the constructed operator.
    for j in range(J + 1):
        extracted = ms(sp.Matrix([
            [
                sp.Poly(B[row, col], z, domain="EX").coeff_monomial(z**j)
                for col in range(2)
            ]
            for row in range(2)
        ]))
        if not is_zero_matrix(ms(extracted - operator_blocks[j])):
            raise AssertionError(f"normal-ordered z^{j} operator block changed")

    # Exact factorial-clearing identity.  If m=n-j then
    #   F_J(n)^2/F_j(n)^2 = F_{J-j}(m)^2.
    # Hence coefficient extraction of z^j P(theta) at z^n evaluates P(n-j)
    # and every lag shares the same denominator (n-J)!^2.
    for j in range(J + 1):
        left = simp(falling(n, J) ** 2 / falling(n, j) ** 2)
        right = simp(falling(n - j, J - j) ** 2)
        if simp(left - right) != 0:
            raise AssertionError(f"factorial clearing identity failed at lag {j}")

        coeff_block = ms(operator_blocks[j].subs(theta, n - j))
        recurrence_block = ms(
            Cj[j].subs(p, alpha + n - j)
            * falling(n - j, J - j) ** 2
            * sp.Matrix([[1, 1], [0, 4 * (n - j) + 2]])
        )
        if not is_zero_matrix(ms(coeff_block - recurrence_block)):
            raise AssertionError(f"coefficient extraction identity failed at lag {j}")

    # Reconstruct the exact physical recurrence coordinates used by the
    # invariant-cone certificate, then test the new operator on n=10,...,60.
    A = ms(Cj[0].subs(p, alpha + n))
    A00 = simp(A[0, 0])
    E = sp.Matrix([1, 0])
    rvec = lambda k: sp.Matrix([1, 2 * (2 * k + 1)])
    lvec = lambda k: sp.Matrix([1, 2 * (2 * k - 3)])

    X_xi, X_kap = {}, {}
    for j in range(1, J + 1):
        block = ms(Cj[j].subs(p, alpha + n - j))
        X_xi[j] = simp(-block[0, 0] / A00)
        X_kap[j] = simp(
            -(
                sp.Matrix([[block[0, 0], block[0, 1]]]) * rvec(n - j)
            )[0]
            / A00
        )

    ell_next = lvec(n + 1)
    C1n = ms(Cj[1].subs(p, alpha + n))
    gamma = simp((ell_next.T * C1n * rvec(n))[0])
    if simp(gamma + sp.Rational(125, 6) * n**2) != 0:
        raise AssertionError("accumulation gamma changed")
    cxi = simp((ell_next.T * C1n * E)[0])
    K_xi = {j: simp(-cxi * X_xi[j] / gamma) for j in range(1, J + 1)}
    K_kap = {j: simp(-cxi * X_kap[j] / gamma) for j in range(1, J + 1)}
    for j in range(2, J + 1):
        lag = j - 1
        block = ms(Cj[j].subs(p, alpha + n + 1 - j))
        K_xi[lag] = simp(
            K_xi.get(lag, 0) - (ell_next.T * block * E)[0] / gamma
        )
        K_kap[lag] = simp(
            K_kap.get(lag, 0)
            - (ell_next.T * block * rvec(n + 1 - j))[0] / gamma
        )

    xi = {0: sp.Rational(0), 1: sp.Rational(20, 27)}
    kap = {0: sp.Rational(0), 1: sp.Rational(-5, 27)}

    def val(tab: dict[int, sp.Expr], k: int) -> sp.Expr:
        return sp.Rational(0) if k < 0 else tab.get(k, sp.Rational(0))

    def ev(expr: sp.Expr, k: int) -> sp.Rational:
        out = sp.cancel(expr.subs(n, k))
        if out.free_symbols:
            raise AssertionError("symbolic parameter survived unit-mass specialization")
        return sp.Rational(out)

    for k in range(2, 61):
        xv = sp.Rational(0)
        kv = sp.Rational(0)
        for j in range(1, J + 1):
            xv += ev(X_xi.get(j, 0), k) * val(xi, k - j)
            xv += ev(X_kap.get(j, 0), k) * val(kap, k - j)
            kv += ev(K_xi.get(j, 0), k) * val(xi, k - j)
            kv += ev(K_kap.get(j, 0), k) * val(kap, k - j)
        xi[k] = sp.cancel(xv)
        kap[k] = sp.cancel(kv)

    U = {
        k: sp.Matrix([
            sp.cancel(xi[k] / sp.factorial(k) ** 2),
            sp.cancel(kap[k] / sp.factorial(k) ** 2),
        ])
        for k in range(61)
    }

    for k in range(J, 61):
        residual = sp.zeros(2, 1)
        for j in range(J + 1):
            residual += operator_blocks[j].subs(theta, k - j) * U[k - j]
        residual = ms(residual)
        if not is_zero_matrix(residual):
            raise AssertionError(
                f"cleared order-2 Borel operator fails physical coefficient n={k}: "
                f"{residual.tolist()}"
            )

    # The clearing factors annihilate every coefficient below the full-lag
    # threshold.  This is why the present operator is an annihilator rather
    # than a minimal solution-equivalent differential system.
    for k in range(J):
        residual = sp.zeros(2, 1)
        for j in range(k + 1):
            residual += operator_blocks[j].subs(theta, k - j) * U[k - j]
        if not is_zero_matrix(ms(residual)):
            raise AssertionError(f"low-degree clearing kernel changed at n={k}")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_CLEARED_BOREL_OPERATOR_CERTIFIED")
    print(f"FINITE_LAG := {J}")
    print("NORMAL_ORDER := z^j left of polynomial(theta)")
    print("BOREL_COORDINATES := U=(Xi,K)^T with Xi_n=xi_n/(n!)^2, K_n=kappa_n/(n!)^2")
    print("COORDINATE_MAP := S(theta)=[[1,1],[0,4*theta+2]]")
    print("CLEARED_OPERATOR := sum_{j=0}^10 z^j*C_j(1/2+theta)*F_{10-j}(theta)^2*S(theta)")
    print(f"Z_DEGREE := {z_degree}")
    print(f"UNREDUCED_THETA_ORDER := {theta_order}")
    print("SYMBOLIC_FACTORIAL_CLEARING := exact for every lag j=0,...,10")
    print("PHYSICAL_PREFIX_COEFFICIENT_CHECK := n=10,...,60 exact")
    print("LOW_DEGREE_KERNEL := coefficients n=0,...,9 annihilated by clearing factors")
    print("BOUNDARY := unreduced annihilator only; no minimal operator, singular-set, analytic-continuation, or Laplace-summability claim")


if __name__ == "__main__":
    main()
