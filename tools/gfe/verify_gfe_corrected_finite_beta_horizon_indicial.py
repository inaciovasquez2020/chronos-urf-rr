#!/usr/bin/env python3
"""Verify the weighted horizon indicial system of the exact finite-beta odd equations.

This verifier starts from the hash-locked corrected AEH=1/2 Fourier-radial
Euler artifact.  It does not use the perturbative beta expansion or a
hand-entered master equation.

Near the Schwarzschild horizon x = r - 2 M, regular ingoing odd metric data in
Schwarzschild coordinates have the weighted Frobenius form

    h0 ~ A x^p,
    h1 ~ B x^(p-1).

The one-power offset is the coordinate Jacobian carried by the radial metric
component.  The physical ingoing exponent for the exp(-i omega t) convention
is p = -2 i M omega.  The purpose of this verifier is to *test* that exponent
against the exact finite-beta Euler equations, not to assume it.
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


def _root_order_and_reduced_value(poly: sp.Poly) -> tuple[int, object]:
    """Return ord_(r-2M)(poly) and the nonzero reduced value at r=2M."""
    order = 0
    current = poly
    while current:
        quotient, remainder = sp.div(current, RING_ROOT)
        if remainder:
            break
        current = quotient
        order += 1
    value = current.eval(2 * M)
    if value == FIELD.zero:
        raise AssertionError("failed to remove complete horizon-root multiplicity")
    return order, value


def _horizon_valuation_and_lead(expr: sp.Expr) -> tuple[int, sp.Expr]:
    """Exact Laurent valuation and leading coefficient at r=2M."""
    numerator, denominator = sp.fraction(sp.together(expr))
    numerator_poly = sp.Poly(numerator, r, domain=FIELD)
    denominator_poly = sp.Poly(denominator, r, domain=FIELD)
    n_order, n_value = _root_order_and_reduced_value(numerator_poly)
    d_order, d_value = _root_order_and_reduced_value(denominator_poly)
    lead = FIELD.to_sympy(FIELD.convert(n_value) / FIELD.convert(d_value))
    return n_order - d_order, sp.cancel(lead)


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


def derive_weighted_horizon_indicial_system() -> tuple[list[int], sp.Matrix, sp.Expr]:
    equations, h = _parse_equations()
    field_shifts = (0, -1)

    row_orders: list[int] = []
    row_terms: list[list[tuple[int, int, int, sp.Expr]]] = []

    for equation in equations:
        terms: list[tuple[int, int, int, sp.Expr]] = []
        for field in range(2):
            for derivative_order in range(5):
                coefficient = sp.diff(equation, h[field][derivative_order])
                if coefficient == 0:
                    continue
                valuation, lead = _horizon_valuation_and_lead(coefficient)
                weighted_order = valuation + field_shifts[field] - derivative_order
                terms.append((field, derivative_order, weighted_order, lead))
        if not terms:
            raise AssertionError("Euler row contains no field-derivative terms")
        row_orders.append(min(term[2] for term in terms))
        row_terms.append(terms)

    matrix = sp.zeros(2, 2)
    for equation_index, terms in enumerate(row_terms):
        leading_order = row_orders[equation_index]
        for field, derivative_order, weighted_order, lead in terms:
            if weighted_order != leading_order:
                continue
            matrix[equation_index, field] += (
                lead * _falling(p + field_shifts[field], derivative_order)
            )

    matrix = matrix.applyfunc(lambda value: sp.factor(sp.cancel(value)))
    determinant = sp.factor(sp.cancel(matrix.det()))
    return row_orders, matrix, determinant


def main() -> None:
    row_orders, matrix, determinant = derive_weighted_horizon_indicial_system()

    if determinant == 0:
        raise AssertionError(
            "leading weighted horizon indicial determinant is identically zero; "
            "a next-order coupled reduction is required"
        )

    physical_ingoing_exponent = -2 * I * M * omega
    physical_residual = sp.factor(
        sp.cancel(determinant.subs(p, physical_ingoing_exponent))
    )
    if physical_residual != 0:
        raise AssertionError(
            "exact finite-beta Euler indicial determinant does not annihilate "
            "the expected horizon-regular ingoing exponent; "
            f"residual={sp.sstr(physical_residual)}"
        )

    print("GFE_CORRECTED_FINITE_BETA_HORIZON_INDICIAL")
    print(f"SOURCE := {SOURCE.relative_to(ROOT)}")
    print("WEIGHTS := h0:x^p, h1:x^(p-1)")
    print(f"ROW_ORDERS := {row_orders}")
    print("INDICIAL_MATRIX :=")
    for row in matrix.tolist():
        print("  [" + ", ".join(sp.sstr(entry) for entry in row) + "]")
    print(f"INDICIAL_DETERMINANT := {sp.sstr(determinant)}")
    print("PHYSICAL_INGOING_EXPONENT := -2*I*M*omega")
    print("PHYSICAL_INGOING_ROOT := passed")


if __name__ == "__main__":
    main()
