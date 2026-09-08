#!/usr/bin/env python3
"""Propagate an exact finite prefix of the canonical ordinary Borel companion.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

For the generalized-Frobenius pair

    x^alpha [V_L(x) log(x) + V_O(x)],

write the cleared Euler operator as

    C(x,p) = sum_{j=0}^J x^j C_j(p).

The exact coefficient equations are

    sum_j C_j(alpha+n-j) v^L_(n-j) = 0,

and

    sum_j C_j(alpha+n-j) v^O_(n-j)
      + sum_j C'_j(alpha+n-j) v^L_(n-j) = 0.

The merged work already fixes the canonical ordinary normalization

    v^O_0 = (1,2)^T,
    v^O_1 = (0,154/45)^T,

and the exact physical top-log sequence.  This verifier reconstructs the
finite-lag matrices from the authoritative Euler artifact, checks the top-log
coefficient equation directly, and then propagates the ordinary coefficients
through n=20 using the rank-one equation at n together with the left-null
compatibility equation at n+1.

This is deliberately a finite exact prefix.  It is meant to expose the
ordinary order-2 Borel tail pattern needed for the next invariant-majorant
step.  It does not infer a tail cone from finite data and does not evaluate the
double-Laplace state or C_grow.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr
import verify_gfe_corrected_exceptional_accumulation_borel_top_log_local_majorant as local


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def build_lag_blocks() -> tuple[list[sp.Matrix], sp.Symbol]:
    equations, h = rr.base._parse_equations()
    p = rr.base.p
    x = sp.symbols("x", positive=True)
    a, b = sp.symbols("a b")

    trial: dict[sp.Expr, sp.Expr] = {}
    for order in range(5):
        trial[h[0][order]] = a * rr.base._falling(p, order) / x**order
        trial[h[1][order]] = b * rr.base._falling(p - 1, order) / x ** (order + 1)

    specialized: list[sp.Expr] = []
    for equation in equations:
        value = equation.xreplace(trial).subs({
            rr.base.r: 2 + x,
            rr.base.M: 1,
            rr.base.omega: rr.base.I / 4,
            rr.base.lam: 6,
            rr.base.beta: sp.Rational(5, 2),
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

    blocks = [
        ms(sp.Matrix([
            [sp.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j) for col in range(2)]
            for row in range(2)
        ]))
        for j in range(J + 1)
    ]
    return blocks, p


def main() -> None:
    Cj, p = build_lag_blocks()
    J = len(Cj) - 1
    alpha = sp.Rational(1, 2)
    N = 20

    xi_l, kap_l = local.physical_prefix()

    def top_log_vector(n: int) -> sp.Matrix:
        if n < 0:
            return sp.zeros(2, 1)
        xi = xi_l.get(n, sp.Rational(0))
        kap = kap_l.get(n, sp.Rational(0))
        return sp.Matrix([xi + kap, (4 * n + 2) * kap])

    # Check the generalized-Frobenius highest-log recurrence directly.  This
    # pins the p-shift convention before the ordinary derivative equation is
    # used.
    for n in range(0, N + 2):
        residual = sp.zeros(2, 1)
        for j in range(J + 1):
            k = n - j
            if k < 0:
                continue
            residual += Cj[j].subs(p, alpha + k) * top_log_vector(k)
        residual = ms(residual)
        if any(value != 0 for value in residual):
            raise AssertionError(
                f"top-log generalized-Frobenius recurrence changed at n={n}: {list(residual)}"
            )

    def ordinary_source(n: int) -> sp.Matrix:
        source = sp.zeros(2, 1)
        for j in range(J + 1):
            k = n - j
            if k < 0:
                continue
            source += Cj[j].diff(p).subs(p, alpha + k) * top_log_vector(k)
        return ms(source)

    ordinary: dict[int, sp.Matrix] = {
        0: sp.Matrix([sp.Integer(1), sp.Integer(2)]),
        1: sp.Matrix([sp.Integer(0), sp.Rational(154, 45)]),
    }

    def equation_residual(n: int, candidate: sp.Matrix | None = None) -> sp.Matrix:
        residual = ordinary_source(n)
        for j in range(J + 1):
            k = n - j
            if k < 0:
                continue
            if k == n and candidate is not None:
                vec = candidate
            else:
                vec = ordinary.get(k)
                if vec is None:
                    raise AssertionError(f"ordinary coefficient v_{k} not available")
            residual += Cj[j].subs(p, alpha + k) * vec
        return ms(residual)

    # The canonical seed must already satisfy the n=0 and n=1 equations.
    for n in (0, 1):
        residual = equation_residual(n)
        if any(value != 0 for value in residual):
            raise AssertionError(
                f"canonical ordinary seed fails generalized-Frobenius equation at n={n}: {list(residual)}"
            )

    for n in range(2, N + 1):
        M = ms(Cj[0].subs(p, alpha + n))
        if M.rank() != 1:
            raise AssertionError(f"ordinary leading matrix rank changed at n={n}: rank={M.rank()}")
        null_right = M.nullspace()
        if len(null_right) != 1:
            raise AssertionError(f"ordinary right-null dimension changed at n={n}")
        rnull = ms(null_right[0])

        known = ordinary_source(n)
        for j in range(1, J + 1):
            k = n - j
            if k < 0:
                continue
            known += Cj[j].subs(p, alpha + k) * ordinary[k]
        known = ms(known)
        rhs = ms(-known)

        # Construct one exact particular solution of M v = rhs from a
        # nonzero row entry, then verify the second row exactly.
        particular: sp.Matrix | None = None
        for row in range(2):
            a0 = simp(M[row, 0])
            b0 = simp(M[row, 1])
            if a0 != 0:
                particular = sp.Matrix([simp(rhs[row] / a0), sp.Integer(0)])
                break
            if b0 != 0:
                particular = sp.Matrix([sp.Integer(0), simp(rhs[row] / b0)])
                break
        if particular is None:
            raise AssertionError(f"ordinary rank-one matrix vanished at n={n}")
        if any(value != 0 for value in ms(M * particular - rhs)):
            raise AssertionError(f"ordinary particular solve inconsistent at n={n}")

        # Equation n leaves the right-null direction free.  The left-null
        # compatibility condition at n+1 fixes it for the canonical branch.
        Mnext = ms(Cj[0].subs(p, alpha + n + 1))
        left_null = Mnext.T.nullspace()
        if len(left_null) != 1:
            raise AssertionError(f"ordinary left-null dimension changed at n+1={n+1}")
        ell = ms(left_null[0])

        rest_next = ordinary_source(n + 1)
        for j in range(2, J + 1):
            k = n + 1 - j
            if k < 0:
                continue
            rest_next += Cj[j].subs(p, alpha + k) * ordinary[k]
        C1n = ms(Cj[1].subs(p, alpha + n))
        coeff = simp((ell.T * C1n * rnull)[0])
        constant = simp((ell.T * (C1n * particular + rest_next))[0])
        if coeff == 0:
            raise AssertionError(
                f"ordinary compatibility failed to fix null coordinate at n={n}; constant={constant}"
            )
        tau = simp(-constant / coeff)
        ordinary[n] = ms(particular + tau * rnull)

        residual = equation_residual(n)
        if any(value != 0 for value in residual):
            raise AssertionError(f"ordinary recurrence residual nonzero at n={n}: {list(residual)}")

        compat = simp((ell.T * (
            C1n * ordinary[n] + rest_next
        ))[0])
        if compat != 0:
            raise AssertionError(f"ordinary n+1 compatibility residual nonzero after n={n}")

    # Convert physical two-vector coefficients back to the Borel recurrence
    # coordinates used by the merged ordinary-companion certificate:
    #   physical v_n = S(n) (xi_n,kappa_n),
    #   S(n)=[[1,1],[0,4n+2]].
    xi_o: dict[int, sp.Expr] = {}
    kap_o: dict[int, sp.Expr] = {}
    bxi_o: dict[int, sp.Expr] = {}
    bkap_o: dict[int, sp.Expr] = {}
    bkap_l: dict[int, sp.Expr] = {}
    for n in range(N + 1):
        a_n = simp(ordinary[n][0])
        b_n = simp(ordinary[n][1])
        kap = simp(b_n / (4 * n + 2))
        xi = simp(a_n - kap)
        kap_o[n] = kap
        xi_o[n] = xi
        bkap_o[n] = simp(kap / sp.factorial(n) ** 2)
        bxi_o[n] = simp(xi / sp.factorial(n) ** 2)
        bkap_l[n] = simp(kap_l.get(n, 0) / sp.factorial(n) ** 2)

    if xi_o[0] != 0 or kap_o[0] != 1:
        raise AssertionError("canonical ordinary n=0 Borel coordinates changed")
    if xi_o[1] != -sp.Rational(77, 135) or kap_o[1] != sp.Rational(77, 135):
        raise AssertionError("canonical ordinary n=1 Borel coordinates changed")

    checkpoints = [2, 4, 8, 12, 16, 20]
    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_PREFIX_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("GENERALIZED_FROBENIUS_TOP_LOG_EQUATION := sum_j C_j(alpha+n-j)*vL_(n-j)=0 checked exactly through n=21")
    print("GENERALIZED_FROBENIUS_ORDINARY_EQUATION := sum_j C_j(alpha+n-j)*vO_(n-j)+C'_j(alpha+n-j)*vL_(n-j)=0")
    print("CANONICAL_ORDINARY_N0_PHYSICAL_VECTOR := [1,2]")
    print("CANONICAL_ORDINARY_N1_PHYSICAL_VECTOR := [0,154/45]")
    print("CANONICAL_ORDINARY_N1_BOREL_COORDINATES := xi=-77/135; kappa=77/135")
    print(f"EXACT_ORDINARY_PREFIX_END := {N}")
    for n in checkpoints:
        ratio = simp(bkap_o[n] / bkap_o[n - 1]) if bkap_o[n - 1] != 0 else sp.nan
        rel_log = simp(bkap_o[n] / bkap_l[n]) if bkap_l[n] != 0 else sp.nan
        print(f"ORDINARY_BOREL_XI_N_{n} := {sp.sstr(bxi_o[n])}")
        print(f"ORDINARY_BOREL_KAPPA_N_{n} := {sp.sstr(bkap_o[n])}")
        print(f"ORDINARY_BOREL_KAPPA_RATIO_N_{n} := {sp.sstr(sp.N(ratio, 24))}")
        print(f"ORDINARY_TO_TOP_LOG_KAPPA_RATIO_N_{n} := {sp.sstr(sp.N(rel_log, 24))}")
    print("FINITE_PREFIX_ONLY := True")
    print("NEXT_ROUTE := use the exact ordinary prefix and recurrence to formulate a rigorous order-2 Borel tail majorant before the local Laplace-state enclosure")
    print("BOUNDARY := no ordinary tail cone, local ordinary uniform bound, double-Laplace numerical enclosure, r=4096 physical-state enclosure, C_grow nonvanishing, or global exceptional-mode closure is claimed")


if __name__ == "__main__":
    main()
