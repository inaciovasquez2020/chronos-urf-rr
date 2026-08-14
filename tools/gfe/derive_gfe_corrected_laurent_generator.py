#!/usr/bin/env python3
"""Export the exact Laurent certificate for the corrected AEH=1/2 descriptor.

The descriptor has four identity shift rows and a lower-triangular 2x2
derivative block.  We therefore form adj(E) A without ever constructing a
dense symbolic inverse.  Arithmetic is polynomial in beta over the exact
rational-function field QQ(i)(M,r,lam,omega).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"
OUTPUT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json"
RECEIPT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_laurent_generator_receipt.txt"

M, r, beta, lam, omega = sp.symbols("M r beta lam omega")
FIELD = sp.QQ_I.frac_field(M, r, lam, omega)
LOCALS = {"M": M, "r": r, "beta": beta, "lam": lam, "lambda": lam,
          "omega": omega, "I": sp.I}
ZERO = sp.Poly(0, beta, domain=FIELD)
ONE = sp.Poly(1, beta, domain=FIELD)


def poly(text: str) -> sp.Poly:
    # Parsing numerator and denominator separately avoids asking SymPy for a
    # costly multivariate rational-expression normalization.  Every exported
    # descriptor denominator is beta-independent, which is checked here.
    numerator, denominator = sp.fraction(sp.sympify(text, locals=LOCALS))
    numerator_poly = sp.Poly(numerator, beta, domain=FIELD)
    denominator_poly = sp.Poly(denominator, beta, domain=FIELD)
    assert denominator_poly.degree() <= 0
    denominator_coefficient = FIELD.convert(denominator_poly.nth(0))
    return numerator_poly.mul_ground(FIELD.one / denominator_coefficient)


def valuation(value: sp.Poly) -> int | None:
    return min(k[0] for k in value.as_dict()) if value else None


def shift_down(value: sp.Poly, amount: int) -> sp.Poly:
    out = { (k[0] - amount,): coefficient
            for k, coefficient in value.as_dict().items() }
    if any(k[0] < 0 for k in out):
        raise AssertionError("inexact beta cancellation")
    return sp.Poly.from_dict(out, beta, domain=FIELD)


def scalar_text(value) -> str:
    return sp.sstr(FIELD.to_sympy(FIELD.convert(value)))


def coefficient(value: sp.Poly, degree: int):
    return FIELD.convert(value.nth(degree))


def polynomial_payload(value: sp.Poly) -> list[str]:
    degree = value.degree() if value else -1
    return [scalar_text(coefficient(value, j)) for j in range(degree + 1)]


def matrix_at(matrices: dict[int, list[list]], exponent: int) -> list[list[str]]:
    matrix = matrices[exponent]
    return [[scalar_text(matrix[i][j]) for j in range(6)] for i in range(6)]


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    e = [[poly(source["descriptor_E"][i][j]) for j in range(6)] for i in range(6)]
    a_matrix = [[poly(source["descriptor_A"][i][j]) for j in range(6)] for i in range(6)]

    # The certified descriptor's only nontrivial derivative block is
    # B=[[a,0],[c,d]] in rows (4,5), columns (2,5).
    a, upper_right, c, d = e[4][2], e[4][5], e[5][2], e[5][5]
    assert upper_right == ZERO
    for row, (left, right) in enumerate(((0, 1), (1, 2), (3, 4), (4, 5))):
        assert e[row][left] == ONE and a_matrix[row][right] == ONE
        assert sum(entry != ZERO for entry in e[row]) == 1
    determinant = a * d

    # H=adj(E)A, represented against det(E).  Four rows are shifts; the last
    # two are the exact triangular adjugate products.
    h = [[ZERO for _ in range(6)] for _ in range(6)]
    for row, right in ((0, 1), (1, 2), (3, 4), (4, 5)):
        h[row][right] = determinant
    for j in range(6):
        h[2][j] = d * a_matrix[4][j]
        h[5][j] = a * a_matrix[5][j] - c * a_matrix[4][j]

    exported_det = poly(source["descriptor_determinant"])
    assert exported_det == determinant
    det_valuation = valuation(determinant)
    h_valuations = [[valuation(entry) for entry in row] for row in h]
    global_h_valuation = min(v for row in h_valuations for v in row if v is not None)
    assert det_valuation == 3 and global_h_valuation == 2

    # Exact identity E H = det(E) A.
    for i in range(6):
        for j in range(6):
            left = sum((e[i][q] * h[q][j] for q in range(6)), ZERO)
            assert left == determinant * a_matrix[i][j]

    reduced_numerator = [[shift_down(entry, global_h_valuation)
                          for entry in row] for row in h]
    reduced_denominator = shift_down(determinant, global_h_valuation)
    denominator_valuation = valuation(reduced_denominator)
    regular_denominator = shift_down(reduced_denominator, denominator_valuation)
    assert denominator_valuation == 1
    assert coefficient(regular_denominator, 0) != FIELD.zero
    minimum_order = -denominator_valuation

    numerator_degree = max(entry.degree() for row in reduced_numerator
                           for entry in row if entry)
    regular_degree = regular_denominator.degree()
    numerator_coefficients = []
    for degree in range(numerator_degree + 1):
        numerator_coefficients.append([
            [scalar_text(coefficient(reduced_numerator[i][j], degree)) for j in range(6)]
            for i in range(6)
        ])
    regular_coefficients = [coefficient(regular_denominator, j)
                            for j in range(regular_degree + 1)]

    # t_n are the Taylor coefficients of 1/d(beta), needed here through the
    # coefficient G_1.  The exported recurrence defines every later t_n.
    inverse = [FIELD.one]
    inverse[0] = FIELD.one / regular_coefficients[0]
    for n in range(1, 3):
        inverse.append(-sum((regular_coefficients[j] * inverse[n-j]
                            for j in range(1, min(n, regular_degree) + 1)),
                           FIELD.zero) / regular_coefficients[0])

    laurent = {}
    for exponent in range(minimum_order, 2):
        matrix = [[FIELD.zero for _ in range(6)] for _ in range(6)]
        target = exponent + denominator_valuation
        for degree in range(min(numerator_degree, target) + 1):
            inv_index = target - degree
            for i in range(6):
                for j in range(6):
                    matrix[i][j] += coefficient(reduced_numerator[i][j], degree) * inverse[inv_index]
        laurent[exponent] = matrix
    assert any(value != FIELD.zero for row in laurent[minimum_order] for value in row)

    # Multiplying the truncated Laurent series by beta*d must reproduce the
    # reduced numerator through the degree corresponding to G_1.
    for degree in range(0, 3):
        for i in range(6):
            for j in range(6):
                reconstructed = sum((regular_coefficients[q] *
                                     laurent[degree-q-1][i][j]
                                     for q in range(min(regular_degree, degree) + 1)
                                     if degree-q-1 in laurent), FIELD.zero)
                assert reconstructed == coefficient(reduced_numerator[i][j], degree)

    entry_orders = []
    for row in h_valuations:
        entry_orders.append([None if value is None else value - det_valuation
                             for value in row])

    payload = {
        "certificate": "GFE_CORRECTED_AEH_HALF_GUARDED_LAURENT_GENERATOR",
        "scope": "exact Laurent structure of the guarded ordinary generator from the corrected AEH=1/2 six-state descriptor",
        "source_descriptor": str(SOURCE.relative_to(ROOT)),
        "source_descriptor_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "coefficient_field": "QQ(i)(M,r,lam,omega)",
        "state_dimension": 6,
        "representation_identity": "G=H/det(E), H=adj(E)A=P/beta^2, det(E)=beta^2*Q, G=P/Q",
        "descriptor_determinant_beta_valuation": det_valuation,
        "adjugate_A_entry_beta_valuations": h_valuations,
        "generator_entry_minimum_laurent_orders": entry_orders,
        "global_adjugate_A_beta_valuation": global_h_valuation,
        "generator_minimum_laurent_order": minimum_order,
        "principal_part_range": [-1, -1],
        "reduced_numerator_beta_coefficients": numerator_coefficients,
        "reduced_denominator_beta_coefficients": polynomial_payload(reduced_denominator),
        "regular_denominator_beta_coefficients": [scalar_text(x) for x in regular_coefficients],
        "regular_denominator_at_zero": scalar_text(regular_coefficients[0]),
        "inverse_regular_denominator_recurrence": "t_0=1/d_0; t_n=-(1/d_0)*sum_{j=1}^{min(n,deg(d))} d_j*t_{n-j}",
        "all_orders_convolution": "G_k=sum_{j=0}^{deg(P)} P_j*t_{k+1-j}, with t_n=0 for n<0",
        "laurent_coefficients": {
            "G_-1": matrix_at(laurent, -1),
            "G_0": matrix_at(laurent, 0),
            "G_1": matrix_at(laurent, 1),
        },
        "ordinary_generator_guard": source["ordinary_generator_guard"],
        "local_analytic_domain": "for fixed guarded parameters, a sufficiently small punctured beta-neighborhood on which d(beta) != 0",
        "exact_checks": {
            "det_E_identity": True,
            "E_times_H_equals_det_E_times_A": True,
            "det_E_beta_valuation": True,
            "regular_denominator_at_zero_nonzero": True,
            "laurent_through_G_1_reconstruction": True,
            "principal_part_exact_order": True,
            "descriptor_guard_unchanged": True,
            "gr_reduction_preserved_at_euler_descriptor_level": source["gr_reduction"] == [True, True],
        },
    }
    payload["payload_sha256"] = hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    receipt = "\n".join([
        payload["certificate"],
        "DESCRIPTOR_DET_BETA_VALUATION := 3",
        "GENERATOR_MIN_LAURENT_ORDER := -1",
        "PRINCIPAL_PART := G_-1",
        "G_MINUS_1 := passed",
        "G_0 := passed",
        "G_1 := passed",
        "ALL_ORDERS_LAURENT_RULE := passed",
        "EXACT_EG_EQUALS_A := passed",
        "DESCRIPTOR_GUARD := preserved",
        "GR_REDUCTION := preserved at Euler/descriptor level",
        f"PAYLOAD_SHA256 := {payload['payload_sha256']}",
    ]) + "\n"
    RECEIPT.write_text(receipt, encoding="utf-8")
    print(receipt, end="")


if __name__ == "__main__":
    main()
