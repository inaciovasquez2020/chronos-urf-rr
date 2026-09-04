#!/usr/bin/env python3
"""Verify the weighted horizon Frobenius system of the exact finite-beta odd equations.

This verifier starts from the hash-locked corrected AEH=1/2 Fourier-radial
Euler artifact.  It does not use the perturbative beta expansion or a
hand-entered master equation.

Near the Schwarzschild horizon x = r - 2 M, regular ingoing odd metric data in
Schwarzschild coordinates have the weighted Frobenius form

    h0 ~ A x^p,
    h1 ~ B x^(p-1).

The one-power offset is the coordinate Jacobian carried by the radial metric
component.  The leading weighted Euler matrix is constrained (rank deficient),
so the exponent is selected by the first subleading solvability condition.
The physical ingoing exponent for the exp(-i omega t) convention is
p = -2 i M omega.  This verifier tests that exponent against the exact
finite-beta equations rather than assuming it.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"

M, beta, lam, omega, r, p = sp.symbols("M beta lam omega r p")
I = sp.I
LOCALS = {
    "M": M,
    "beta": beta,
    "lam": lam,
    "lambda": lam,
    "omega": omega,
    "r": r,
    "I": I,
}
FIELD = sp.QQ_I.frac_field(M, beta, lam, omega)
RING_ROOT = sp.Poly(r - 2 * M, r, domain=FIELD)


def _falling(z: sp.Expr, order: int) -> sp.Expr:
    out = sp.Integer(1)
    for j in range(order):
        out *= z - j
    return sp.expand(out)


def _root_order_and_reduced_poly(poly: sp.Poly) -> tuple[int, sp.Poly]:
    """Remove the complete (r-2M) multiplicity from a nonzero polynomial."""
    order = 0
    current = poly
    while current:
        quotient, remainder = sp.div(current, RING_ROOT)
        if remainder:
            break
        current = quotient
        order += 1
    if current.eval(2 * M) == FIELD.zero:
        raise AssertionError("failed to remove complete horizon-root multiplicity")
    return order, current


def _horizon_valuation_lead_next(expr: sp.Expr) -> tuple[int, sp.Expr, sp.Expr]:
    """Exact valuation plus the first two Laurent coefficients at r=2M."""
    numerator, denominator = sp.fraction(sp.together(expr))
    numerator_poly = sp.Poly(numerator, r, domain=FIELD)
    denominator_poly = sp.Poly(denominator, r, domain=FIELD)
    n_order, n_reduced = _root_order_and_reduced_poly(numerator_poly)
    d_order, d_reduced = _root_order_and_reduced_poly(denominator_poly)

    n0 = FIELD.convert(n_reduced.eval(2 * M))
    d0 = FIELD.convert(d_reduced.eval(2 * M))
    n1 = FIELD.convert(n_reduced.diff().eval(2 * M))
    d1 = FIELD.convert(d_reduced.diff().eval(2 * M))

    lead = n0 / d0
    next_coefficient = (n1 * d0 - n0 * d1) / (d0 * d0)
    return (
        n_order - d_order,
        sp.cancel(FIELD.to_sympy(lead)),
        sp.cancel(FIELD.to_sympy(next_coefficient)),
    )


def _parse_equations() -> tuple[list[sp.Expr], list[list[sp.Symbol]]]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    h = [
        [sp.Symbol(f"h{field}r{order}") for order in range(5)]
        for field in range(2)
    ]
    local_map = dict(LOCALS)
    local_map.update({str(symbol): symbol for row in h for symbol in row})
    equations = [
        sp.sympify(text, locals=local_map)
        for text in source["euler_equations"]
    ]
    return equations, h


def _right_kernel_vector(matrix: sp.Matrix) -> sp.Matrix:
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    if a != 0 or b != 0:
        return sp.Matrix([-b, a])
    if c != 0 or d != 0:
        return sp.Matrix([-d, c])
    raise AssertionError("leading weighted horizon matrix is identically zero")


def _left_kernel_vector(matrix: sp.Matrix) -> sp.Matrix:
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    if a != 0 or c != 0:
        return sp.Matrix([-c, a])
    if b != 0 or d != 0:
        return sp.Matrix([-d, b])
    raise AssertionError("shifted leading weighted horizon matrix is identically zero")


def derive_weighted_horizon_frobenius_system() -> tuple[
    list[int], sp.Matrix, sp.Matrix, sp.Expr
]:
    equations, h = _parse_equations()
    field_shifts = (0, -1)

    row_orders: list[int] = []
    row_terms: list[list[tuple[int, int, int, sp.Expr, sp.Expr]]] = []

    for equation in equations:
        terms: list[tuple[int, int, int, sp.Expr, sp.Expr]] = []
        for field in range(2):
            for derivative_order in range(5):
                coefficient = sp.diff(equation, h[field][derivative_order])
                if coefficient == 0:
                    continue
                valuation, lead, next_coefficient = _horizon_valuation_lead_next(
                    coefficient
                )
                weighted_order = valuation + field_shifts[field] - derivative_order
                terms.append(
                    (field, derivative_order, weighted_order, lead, next_coefficient)
                )
        if not terms:
            raise AssertionError("Euler row contains no field-derivative terms")
        row_orders.append(min(term[2] for term in terms))
        row_terms.append(terms)

    leading = sp.zeros(2, 2)
    subleading = sp.zeros(2, 2)
    for equation_index, terms in enumerate(row_terms):
        leading_order = row_orders[equation_index]
        for field, derivative_order, weighted_order, lead, next_coefficient in terms:
            falling = _falling(p + field_shifts[field], derivative_order)
            if weighted_order == leading_order:
                leading[equation_index, field] += lead * falling
                subleading[equation_index, field] += next_coefficient * falling
            elif weighted_order == leading_order + 1:
                subleading[equation_index, field] += lead * falling

    leading = leading.applyfunc(lambda value: sp.factor(sp.cancel(value)))
    subleading = subleading.applyfunc(lambda value: sp.factor(sp.cancel(value)))

    leading_determinant = sp.factor(sp.cancel(leading.det()))
    if leading_determinant != 0:
        raise AssertionError(
            "expected constrained leading weighted horizon system, but its "
            f"determinant is {sp.sstr(leading_determinant)}"
        )

    seed = _right_kernel_vector(leading)
    if any(sp.factor(sp.cancel(value)) != 0 for value in leading * seed):
        raise AssertionError("constructed leading right-kernel vector is invalid")

    shifted_leading = leading.subs(p, p + 1).applyfunc(
        lambda value: sp.factor(sp.cancel(value))
    )
    left_null = _left_kernel_vector(shifted_leading)
    if any(
        sp.factor(sp.cancel(value)) != 0
        for value in (left_null.T * shifted_leading)
    ):
        raise AssertionError("constructed shifted left-kernel vector is invalid")

    compatibility = sp.factor(
        sp.cancel((left_null.T * subleading * seed)[0])
    )
    return row_orders, leading, subleading, compatibility


def main() -> None:
    row_orders, leading, subleading, compatibility = (
        derive_weighted_horizon_frobenius_system()
    )

    if compatibility == 0:
        raise AssertionError(
            "first subleading horizon compatibility is identically zero; "
            "one more Frobenius order is required"
        )

    physical_ingoing_exponent = -2 * I * M * omega
    physical_residual = sp.factor(
        sp.cancel(compatibility.subs(p, physical_ingoing_exponent))
    )
    if physical_residual != 0:
        raise AssertionError(
            "exact finite-beta subleading horizon compatibility does not "
            "annihilate the expected horizon-regular ingoing exponent; "
            f"residual={sp.sstr(physical_residual)}"
        )

    print("GFE_CORRECTED_FINITE_BETA_HORIZON_FROBENIUS")
    print(f"SOURCE := {SOURCE.relative_to(ROOT)}")
    print("WEIGHTS := h0:x^p, h1:x^(p-1)")
    print(f"ROW_ORDERS := {row_orders}")
    print("LEADING_MATRIX :=")
    for row in leading.tolist():
        print("  [" + ", ".join(sp.sstr(entry) for entry in row) + "]")
    print("SUBLEADING_MATRIX :=")
    for row in subleading.tolist():
        print("  [" + ", ".join(sp.sstr(entry) for entry in row) + "]")
    print(f"FROBENIUS_COMPATIBILITY := {sp.sstr(compatibility)}")
    print("PHYSICAL_INGOING_EXPONENT := -2*I*M*omega")
    print("PHYSICAL_INGOING_ROOT := passed")


if __name__ == "__main__":
    main()
