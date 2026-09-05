#!/usr/bin/env python3
"""Certify the complete rational denominator support of the reduced Borel rows.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The preceding verifier constructs the exact cleared order-2 Borel annihilator
and reduces its two rows by three elementary left Ore operations in Q(z)<theta>,
with theta=z d/dz.  This verifier reconstructs that reduction independently
from the same hash-locked Euler artifact and inspects *every* coefficient of
every theta power in the reduced rows.

The goal is deliberately narrower than analytic continuation: certify that the
lower-order rational coefficients introduce no finite pole away from z=0.
Together with the already certified reduced row-leading determinant

  625*z*(18*z+5)/64,

this isolates -5/18 as the only nonzero row-leading degeneracy while keeping
z=0 separate as the rational row-transform pole.
"""
from __future__ import annotations

import sympy as sp
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def reconstruct_reduced_rows() -> tuple[list[list[sp.Expr]], sp.Symbol, sp.Symbol, list[tuple[int, int, int, sp.Expr]]]:
    equations, h = rr.base._parse_equations()
    p = rr.base.p
    x = sp.symbols("x", positive=True)
    z, theta = sp.symbols("z theta")
    a, b = sp.symbols("a b")

    trial = {}
    for order in range(5):
        trial[h[0][order]] = a * rr.base._falling(p, order) / x**order
        trial[h[1][order]] = b * rr.base._falling(p - 1, order) / x ** (order + 1)

    specialized = []
    for equation in equations:
        q = equation.xreplace(trial).subs({
            rr.base.r: 2 + x,
            rr.base.M: 1,
            rr.base.omega: rr.base.I / 4,
            rr.base.lam: 6,
            rr.base.beta: sp.Rational(5, 2),
        })
        specialized.append(rr.simp(q))
    q0, q1 = specialized

    F = rr.ms(sp.Matrix([
        [sp.diff(rr.simp(x**3 * q0), a), sp.diff(rr.simp(x**3 * q0), b)],
        [sp.diff(rr.simp(x**2 * q1), a), sp.diff(rr.simp(x**2 * q1), b)],
    ]))
    Dp = sp.Poly(1, x, domain="EX")
    for entry in F:
        _, den = sp.fraction(rr.simp(entry))
        Dp = sp.lcm(Dp, sp.Poly(den, x, domain="EX").monic())
    D = rr.simp(Dp.as_expr() / Dp.as_expr().subs(x, 0))
    C = rr.ms(D * F)
    J = max(sp.Poly(entry, x, domain="EX").degree() for entry in C if entry != 0)
    if J != 10:
        raise AssertionError(f"finite lag changed: {J}")

    Cj = [
        rr.ms(sp.Matrix([
            [sp.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j) for col in range(2)]
            for row in range(2)
        ]))
        for j in range(J + 1)
    ]

    alpha = sp.Rational(1, 2)
    S = sp.Matrix([[1, 1], [0, 4 * theta + 2]])
    B = sp.zeros(2, 2)
    for j in range(J + 1):
        B += z**j * rr.ms(
            Cj[j].subs(p, alpha + theta)
            * rr.falling(theta, J - j) ** 2
            * S
        )
    B = B.applyfunc(sp.expand)

    rows = [[B[i, 0], B[i, 1]] for i in range(2)]
    if [rr.row_order(row, theta) for row in rows] != [24, 23]:
        raise AssertionError("unreduced row orders changed")

    steps: list[tuple[int, int, int, sp.Expr]] = []
    for _ in range(64):
        orders = [rr.row_order(row, theta) for row in rows]
        if min(orders) < 0:
            break
        if orders[0] == orders[1]:
            high_i, low_i = 1, 0
        elif orders[0] > orders[1]:
            high_i, low_i = 0, 1
        else:
            high_i, low_i = 1, 0
        shift = orders[high_i] - orders[low_i]
        low_shifted = rr.theta_left_row(rows[low_i], z, theta, shift)
        q = rr.proportional_ratio(
            rr.leading_vector(rows[high_i], theta),
            rr.leading_vector(low_shifted, theta),
        )
        if q is None:
            break
        transformed = [
            rr.simp(rows[high_i][column] - q * low_shifted[column])
            for column in range(2)
        ]
        if rr.row_order(transformed, theta) >= orders[high_i]:
            raise AssertionError("Ore cancellation did not lower row order")
        rows[high_i] = transformed
        steps.append((high_i, low_i, shift, rr.simp(q)))
    else:
        raise AssertionError("Ore reduction exceeded step bound")

    expected_steps = [
        (0, 1, 1, sp.Integer(-4)),
        (1, 0, 0, sp.Rational(1, 6)),
        (0, 1, 2, -sp.Rational(18, 7) / z),
    ]
    if len(steps) != len(expected_steps):
        raise AssertionError(f"Ore reduction step count changed: {len(steps)}")
    for actual, expected in zip(steps, expected_steps):
        if actual[:3] != expected[:3] or not rr.is_zero_expr(actual[3] - expected[3]):
            raise AssertionError(f"Ore reduction sequence changed: {steps}")

    reduced_orders = [rr.row_order(row, theta) for row in rows]
    if reduced_orders != [22, 21]:
        raise AssertionError(f"reduced row orders changed: {reduced_orders}")
    return rows, z, theta, steps


def denominator_data(rows: list[list[sp.Expr]], z: sp.Symbol, theta: sp.Symbol) -> tuple[list[sp.Expr], sp.Expr, int, int]:
    row_lcms: list[sp.Expr] = []
    global_lcm = sp.Poly(1, z, domain="QQ")
    nonconstant_denominators = 0
    max_origin_pole_order = 0

    for row in rows:
        row_lcm = sp.Poly(1, z, domain="QQ")
        for entry in row:
            if rr.is_zero_expr(entry):
                continue
            poly_theta = sp.Poly(sp.expand(entry), theta, domain="EX")
            for _, coeff in poly_theta.terms():
                _, den = sp.fraction(sp.cancel(sp.together(coeff)))
                den_poly = sp.Poly(den, z, domain="QQ")
                if den_poly.degree() <= 0:
                    continue
                nonconstant_denominators += 1
                _, factors = sp.factor_list(den_poly.as_expr(), z)
                for factor, exponent in factors:
                    factor_poly = sp.Poly(factor, z, domain="QQ").monic()
                    if factor_poly != sp.Poly(z, z, domain="QQ").monic():
                        raise AssertionError(
                            "hidden reduced-row denominator factor away from z=0: "
                            f"{sp.sstr(factor)}"
                        )
                    max_origin_pole_order = max(max_origin_pole_order, int(exponent))
                row_lcm = sp.lcm(row_lcm, den_poly.monic())
                global_lcm = sp.lcm(global_lcm, den_poly.monic())
        row_lcms.append(sp.factor(row_lcm.as_expr()))

    if nonconstant_denominators == 0:
        raise AssertionError("expected the certified z=0 row-transform pole to survive")

    # Complete clearing check: multiplying by the exact global denominator must
    # make every coefficient polynomial in z, coefficient-by-coefficient in theta.
    global_expr = sp.factor(global_lcm.as_expr())
    for row in rows:
        for entry in row:
            if rr.is_zero_expr(entry):
                continue
            poly_theta = sp.Poly(sp.expand(global_expr * entry), theta, domain="EX")
            for _, coeff in poly_theta.terms():
                _, den = sp.fraction(sp.cancel(sp.together(coeff)))
                if sp.Poly(den, z, domain="QQ").degree() > 0:
                    raise AssertionError(
                        "global reduced-row denominator failed to clear a lower-order coefficient"
                    )

    return row_lcms, global_expr, nonconstant_denominators, max_origin_pole_order


def main() -> None:
    rows, z, theta, steps = reconstruct_reduced_rows()
    row_lcms, global_lcm, nonconstant_count, max_origin_pole_order = denominator_data(
        rows, z, theta
    )

    leads = [rr.leading_vector(row, theta) for row in rows]
    lead_det = rr.simp(
        leads[0][0] * leads[1][1] - leads[0][1] * leads[1][0]
    )
    expected_lead_det = sp.Rational(625, 64) * z * (18 * z + 5)
    if not rr.is_zero_expr(lead_det - expected_lead_det):
        raise AssertionError(f"reduced row-leading determinant changed: {sp.sstr(lead_det)}")

    if rr.is_zero_expr(lead_det.subs(z, -sp.Rational(5, 18))) is False:
        raise AssertionError("-5/18 ceased to be a reduced row-leading zero")
    if rr.is_zero_expr(lead_det.subs(z, 0)) is False:
        raise AssertionError("z=0 ceased to be a reduced row-leading zero")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_REDUCED_DENOMINATORS_CERTIFIED")
    print(f"REDUCED_ROW_THETA_ORDERS := {[rr.row_order(row, theta) for row in rows]}")
    print(f"ORE_REDUCTION_STEPS := {len(steps)}")
    print(f"ROW_DENOMINATOR_LCMS := {[sp.sstr(value) for value in row_lcms]}")
    print(f"GLOBAL_REDUCED_ROW_DENOMINATOR_LCM := {sp.sstr(global_lcm)}")
    print("COMPLETE_LOWER_ORDER_DENOMINATOR_SUPPORT := {z=0}")
    print(f"NONCONSTANT_DENOMINATOR_COEFFICIENT_COUNT := {nonconstant_count}")
    print(f"MAX_ORIGIN_POLE_ORDER_IN_REDUCED_ROWS := {max_origin_pole_order}")
    print("LOWER_ORDER_FINITE_POLES_AWAY_FROM_ORIGIN := none")
    print("REDUCED_ROW_LEADING_DETERMINANT := 625*z*(18*z+5)/64")
    print("REDUCED_ROW_LEADING_ZERO_SET := {0,-5/18}")
    print("NONZERO_ROW_LEADING_DEGENERACY := -5/18")
    print("BOUNDARY := complete reduced-row rational denominator support certified; first-order meromorphic system, genuine-singularity classification, analytic continuation, and Laplace summability remain unproved")


if __name__ == "__main__":
    main()
