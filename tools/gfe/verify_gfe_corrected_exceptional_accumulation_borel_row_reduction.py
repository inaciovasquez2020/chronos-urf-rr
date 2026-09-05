#!/usr/bin/env python3
"""Audit solution-preserving Ore row reduction of the cleared Borel operator.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The previous verifier certifies the normal-ordered annihilator

  B(z,theta)=sum_{j=0}^10 z^j C_j(1/2+theta) F_{10-j}(theta)^2 S(theta),
  theta=z d/dz.

This audit performs only elementary *left* row operations in Q(z)<theta>:

  R_i <- R_i - q(z) theta^k R_j,

while retaining R_j.  Such a step is unimodular: its inverse is obtained by
adding the same q(z) theta^k R_j back.  The noncommutative rule

  theta f(z) = f(z) theta + z f'(z)

is implemented exactly, so no commuting of theta through z-dependent
coefficients is assumed.  A reduction is made only when the complete highest-
theta row vectors are exactly proportional over Q(z).

The result is an exact row-module reduction audit, not yet a minimal scalar
operator or a singular-set certificate.  Poles of rational row multipliers are
reported explicitly and are not classified as genuine Borel singularities.
"""
from __future__ import annotations

import sympy as sp
import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(x: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(x)))


def ms(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


def is_zero_expr(x: sp.Expr) -> bool:
    return simp(x) == 0


def is_zero_row(row: list[sp.Expr]) -> bool:
    return all(is_zero_expr(x) for x in row)


def falling(q: sp.Expr, order: int) -> sp.Expr:
    out = sp.Integer(1)
    for s in range(order):
        out *= q - s
    return sp.expand(out)


def theta_degree(expr: sp.Expr, theta: sp.Symbol) -> int:
    if is_zero_expr(expr):
        return -1
    return int(sp.Poly(sp.expand(expr), theta, domain="EX").degree())


def row_order(row: list[sp.Expr], theta: sp.Symbol) -> int:
    return max(theta_degree(x, theta) for x in row)


def coeff_theta(expr: sp.Expr, theta: sp.Symbol, degree: int) -> sp.Expr:
    if degree < 0 or is_zero_expr(expr):
        return sp.Integer(0)
    return simp(sp.Poly(sp.expand(expr), theta, domain="EX").coeff_monomial(theta**degree))


def leading_vector(row: list[sp.Expr], theta: sp.Symbol) -> list[sp.Expr]:
    d = row_order(row, theta)
    if d < 0:
        return [sp.Integer(0), sp.Integer(0)]
    return [coeff_theta(x, theta, d) for x in row]


def theta_left_expr(expr: sp.Expr, z: sp.Symbol, theta: sp.Symbol) -> sp.Expr:
    """Return theta*expr in normal order with powers of theta on the right."""
    if is_zero_expr(expr):
        return sp.Integer(0)
    poly = sp.Poly(sp.expand(expr), theta, domain="EX")
    out = sp.Integer(0)
    for (k,), coeff in poly.terms():
        out += coeff * theta ** (k + 1)
        out += z * sp.diff(coeff, z) * theta**k
    return simp(out)


def theta_left_row(row: list[sp.Expr], z: sp.Symbol, theta: sp.Symbol, power: int) -> list[sp.Expr]:
    out = list(row)
    for _ in range(power):
        out = [theta_left_expr(x, z, theta) for x in out]
    return out


def proportional_ratio(high: list[sp.Expr], low: list[sp.Expr]) -> sp.Expr | None:
    """Return q with high=q*low, or None if the vectors are not proportional."""
    pivot = None
    for i in range(2):
        if not is_zero_expr(low[i]):
            pivot = i
            break
    if pivot is None:
        return None
    q = simp(high[pivot] / low[pivot])
    for i in range(2):
        if not is_zero_expr(high[i] - q * low[i]):
            return None
    return q


def main() -> None:
    equations, h = base._parse_equations()
    p = base.p
    x = sp.symbols("x", positive=True)
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
            [sp.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j) for col in range(2)]
            for row in range(2)
        ]))
        for j in range(J + 1)
    ]

    alpha = sp.Rational(1, 2)
    S = sp.Matrix([[1, 1], [0, 4 * theta + 2]])
    B = sp.zeros(2, 2)
    for j in range(J + 1):
        B += z**j * ms(Cj[j].subs(p, alpha + theta) * falling(theta, J - j) ** 2 * S)
    B = B.applyfunc(lambda e: sp.expand(e))

    rows = [[B[i, 0], B[i, 1]] for i in range(2)]
    original_rows = [list(r) for r in rows]
    initial_orders = [row_order(r, theta) for r in rows]
    if max(initial_orders) != 24:
        raise AssertionError(f"unreduced theta order changed: {initial_orders}")

    steps: list[tuple[int, int, int, sp.Expr]] = []
    pole_denominators: list[sp.Expr] = []

    # Weak row-Popov style reduction: cancel a complete leading row vector only
    # when it lies exactly in the Q(z)-span of the other leading row vector.
    for _ in range(64):
        orders = [row_order(r, theta) for r in rows]
        if min(orders) < 0:
            break
        if orders[0] == orders[1]:
            high_i, low_i = 1, 0
        elif orders[0] > orders[1]:
            high_i, low_i = 0, 1
        else:
            high_i, low_i = 1, 0
        shift = orders[high_i] - orders[low_i]
        if shift < 0:
            raise AssertionError("internal row-order selection error")

        high_lead = leading_vector(rows[high_i], theta)
        low_shifted = theta_left_row(rows[low_i], z, theta, shift)
        low_lead = leading_vector(low_shifted, theta)
        q = proportional_ratio(high_lead, low_lead)
        if q is None:
            break

        before = list(rows[high_i])
        transformed = [simp(before[c] - q * low_shifted[c]) for c in range(2)]
        if row_order(transformed, theta) >= orders[high_i]:
            raise AssertionError("purported Ore row reduction did not lower row order")

        # Exact inverse certificate for this elementary unimodular operation.
        recovered = [simp(transformed[c] + q * low_shifted[c]) for c in range(2)]
        if any(not is_zero_expr(recovered[c] - before[c]) for c in range(2)):
            raise AssertionError("elementary Ore row operation failed inverse check")

        rows[high_i] = transformed
        steps.append((high_i, low_i, shift, q))
        _, qden = sp.fraction(sp.cancel(sp.together(q)))
        pole_denominators.append(sp.factor(qden))
    else:
        raise AssertionError("Ore row reduction exceeded step bound")

    reduced_orders = [row_order(r, theta) for r in rows]
    if max(reduced_orders) > max(initial_orders):
        raise AssertionError("row reduction increased maximal theta order")

    # Reconstruct the original row module by applying inverse elementary steps
    # in reverse order.  This checks the accumulated noncommutative bookkeeping,
    # not merely each local cancellation.
    recovered_rows = [list(r) for r in rows]
    for high_i, low_i, shift, q in reversed(steps):
        low_shifted = theta_left_row(recovered_rows[low_i], z, theta, shift)
        recovered_rows[high_i] = [
            simp(recovered_rows[high_i][c] + q * low_shifted[c]) for c in range(2)
        ]
    for i in range(2):
        for c in range(2):
            if not is_zero_expr(recovered_rows[i][c] - original_rows[i][c]):
                raise AssertionError("accumulated Ore inverse failed to recover original operator")

    final_leads = [leading_vector(r, theta) for r in rows]
    lead_det = simp(final_leads[0][0] * final_leads[1][1] - final_leads[0][1] * final_leads[1][0])

    pole_poly = sp.Integer(1)
    for den in pole_denominators:
        pole_poly = sp.lcm(sp.Poly(pole_poly, z, domain="QQ"), sp.Poly(den, z, domain="QQ")).as_expr()
    pole_poly = sp.factor(pole_poly)

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORE_ROW_REDUCTION_AUDIT")
    print(f"INITIAL_ROW_THETA_ORDERS := {initial_orders}")
    print(f"UNIMODULAR_ROW_REDUCTION_STEPS := {len(steps)}")
    for idx, (high_i, low_i, shift, q) in enumerate(steps, start=1):
        print(f"STEP_{idx} := R{high_i} <- R{high_i} - ({sp.sstr(q)})*theta^{shift}*R{low_i}")
    print(f"REDUCED_ROW_THETA_ORDERS := {reduced_orders}")
    print(f"REDUCED_MAX_THETA_ORDER := {max(reduced_orders)}")
    print(f"REDUCED_LEADING_ROW_DETERMINANT := {sp.sstr(lead_det)}")
    print(f"ROW_TRANSFORM_POLE_POLYNOMIAL := {sp.sstr(pole_poly)}")
    print("ORE_RULE := theta*f(z)=f(z)*theta+z*f'(z) implemented exactly")
    print("ROW_MODULE_EQUIVALENCE := exact over Q(z)<theta> by elementary determinant-one row operations")
    print("ACCUMULATED_INVERSE_CHECK := exact")
    print("BOUNDARY := row-module reduction only; rational row-transform poles are not classified as genuine Borel singularities; no minimal scalar operator, analytic continuation, or Laplace summability claim")


if __name__ == "__main__":
    main()
