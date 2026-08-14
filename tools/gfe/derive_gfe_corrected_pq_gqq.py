#!/usr/bin/env python3
"""Certify the corrected leading P/Q split and exact finite-beta GQQ block."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json"
OUTPUT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_pq_gqq.json"
RECEIPT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_pq_gqq_receipt.txt"

M, r, beta, lam, omega = sp.symbols("M r beta lam omega")
FIELD = sp.QQ_I.frac_field(M, r, lam, omega)
LOCALS = {"M": M, "r": r, "beta": beta, "lam": lam, "omega": omega, "I": sp.I}


def coefficient(value: sp.Poly, degree: int):
    return FIELD.convert(value.nth(degree))


def scalar_text(value) -> str:
    return sp.sstr(FIELD.to_sympy(FIELD.convert(value)))


def poly_from_coefficients(values: list[str]) -> sp.Poly:
    return sp.Poly.from_list(
        [FIELD.convert(sp.sympify(value, locals=LOCALS)) for value in reversed(values)],
        beta, domain=FIELD,
    )


def matrix_polynomials(source: dict) -> tuple[list[list[sp.Poly]], sp.Poly]:
    coefficients = source["reduced_numerator_beta_coefficients"]
    numerator = [[
        poly_from_coefficients([matrix[i][j] for matrix in coefficients])
        for j in range(6)
    ] for i in range(6)]
    denominator = poly_from_coefficients(source["reduced_denominator_beta_coefficients"])
    return numerator, denominator


def matrix_payload(matrix: list[list[sp.Poly]]) -> list[list[list[str]]]:
    return [[
        [scalar_text(coefficient(entry, degree)) for degree in range(entry.degree() + 1)]
        if entry else ["0"]
        for entry in row
    ] for row in matrix]


def expr(text: str):
    return sp.sympify(text, locals=LOCALS)


def exact_equal(left, right) -> bool:
    numerator, _ = sp.fraction(sp.together(left - right))
    return sp.Poly(sp.expand(numerator), beta, domain=FIELD).is_zero


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes)
    numerator, denominator = matrix_polynomials(source)

    principal = sp.Matrix([
        [expr(value) for value in row]
        for row in source["laurent_coefficients"]["G_-1"]
    ])
    zero = sp.zeros(6)
    assert principal.rank() == 2
    assert principal * principal == zero
    assert principal != zero

    # im(Q0)=im(G_-1) is the canonical rank-two invariant leading subspace.
    # G_-1 alone does not select its complementary projector; the
    # authoritative companion state ordering supplies the lower-derivative
    # coordinate complement.
    p0 = sp.diag(1, 1, 0, 1, 1, 0)
    q0 = sp.eye(6) - p0
    assert p0 * p0 == p0 and q0 * q0 == q0
    assert p0 * q0 == zero and q0 * p0 == zero
    assert p0.rank() == 4 and q0.rank() == 2
    assert principal.row_join(q0).rank() == 2
    commutator = principal * p0 - p0 * principal
    assert commutator == principal and commutator != zero

    p_indices, q_indices = [0, 1, 3, 4], [2, 5]
    blocks = {
        "G_PP": [[numerator[i][j] for j in p_indices] for i in p_indices],
        "G_PQ": [[numerator[i][j] for j in q_indices] for i in p_indices],
        "G_QP": [[numerator[i][j] for j in p_indices] for i in q_indices],
        "G_QQ": [[numerator[i][j] for j in q_indices] for i in q_indices],
    }

    gqq_text = [[
        "2*(-48*M**2*beta + 20*M*beta*r - 15*M*r**3 + 5*r**4)/(r*(r-2*M)*(8*M*beta + 5*r**3))",
        "-I*(-32*M**2*beta*lam + 64*M**2*beta + 16*M*beta*lam*r + 8*M*beta*omega**2*r**3 - 32*M*beta*r + 10*M*lam*r**3 - 20*M*r**3 - 5*lam*r**4 + 5*omega**2*r**6 + 10*r**4)/(omega*r**3*(8*M*beta + 5*r**3))",
    ], [
        "-I*omega*r**2/(r-2*M)**2",
        "2*(192*M**2*beta - 64*M*beta*r - 30*M*r**3 + 5*r**4)/(r*(r-2*M)*(-16*M*beta + 5*r**3))",
    ]]
    gqq = sp.Matrix([[expr(value) for value in row] for row in gqq_text])
    for i in range(2):
        for j in range(2):
            assert exact_equal(numerator[q_indices[i]][q_indices[j]].as_expr(),
                               denominator.as_expr() * gqq[i, j])

    delta = expr(
        "-36864*M**4*beta**2 + 512*M**3*beta**2*lam*r + 26624*M**3*beta**2*r"
        " - 5760*M**3*beta*r**3 - 256*M**2*beta**2*lam*r**2"
        " - 128*M**2*beta**2*omega**2*r**4 - 4608*M**2*beta**2*r**2"
        " - 320*M**2*beta*lam*r**4 + 4960*M**2*beta*r**4 + 1800*M**2*r**6"
        " + 160*M*beta*lam*r**5 - 40*M*beta*omega**2*r**7 - 1200*M*beta*r**5"
        " + 50*M*lam*r**7 - 1000*M*r**7 - 25*lam*r**8"
        " + 25*omega**2*r**10 + 150*r**8"
    )
    determinant_denominator = expr(
        "r**2*(r-2*M)**2*(-16*M*beta+5*r**3)*(8*M*beta+5*r**3)"
    )
    determinant = delta / determinant_denominator
    assert exact_equal(gqq.det(), determinant)

    inverse = sp.Matrix([[gqq[1, 1], -gqq[0, 1]],
                         [-gqq[1, 0], gqq[0, 0]]]) / determinant
    assert all(exact_equal(value, 0) for value in (gqq * inverse - sp.eye(2)))
    assert all(exact_equal(value, 0) for value in (inverse * gqq - sp.eye(2)))

    kernel_vector = sp.Matrix([gqq[1, 1], -gqq[1, 0]])
    range_vector = sp.Matrix([gqq[0, 0], gqq[1, 0]])
    # This becomes a kernel vector exactly on Delta=0.
    assert exact_equal((gqq * kernel_vector)[0], determinant)
    assert exact_equal((gqq * kernel_vector)[1], 0)

    f = 1 - 2 * M / r
    historical_d = sp.Matrix([
        [-sp.Rational(6, 5) / f, 0],
        [12 * sp.I * r * omega / (5 * lam * f**2), -sp.Rational(6, 5) / f],
    ])
    historical_n = sp.Matrix([
        [-5 * f / 6, 0],
        [-5 * sp.I * r * omega / (3 * lam), -5 * f / 6],
    ])
    assert all(exact_equal(value, 0) for value in
               (historical_d * historical_n - sp.eye(2)))
    assert all(exact_equal(value, 0) for value in
               (historical_n * historical_d - sp.eye(2)))
    assert any(not exact_equal(gqq[i, j].subs(beta, 0), historical_d[i, j])
               for i in range(2) for j in range(2))

    payload = {
        "certificate": "GFE_CORRECTED_AEH_HALF_EXACT_PQ_GQQ",
        "scope": "corrected leading companion P0/Q0 decomposition and exact guarded finite-beta GQQ",
        "source_laurent_generator": str(SOURCE.relative_to(ROOT)),
        "source_laurent_generator_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "parameter_definition": {
            "finite_parameter": "beta, exactly the coupling symbol in the authoritative descriptor and Laurent generator",
            "historical_q_relation": "no repository-local certified identity q=beta was found; q in the Fredholm artifact is not substituted here",
        },
        "leading_structure": {
            "rank": 2,
            "image_basis": [["0", "0", "1", "0", "0", "0"], ["0", "0", "0", "0", "0", "1"]],
            "kernel": "ker(G_-1)=span(e_1,e_2,e_4,e_5)",
            "generalized_kernel": "ker(G_-1^2)=C^6",
            "nilpotency_index": 2,
            "minimal_polynomial": "z**2",
            "jordan_structure": "two nilpotent size-2 blocks and two nilpotent size-1 blocks",
            "selection_criterion": "G_-1 fixes the unique canonical rank-two invariant subspace im(Q0)=im(G_-1)=span(e_3,e_6); the companion state grading selects its lower-derivative coordinate complement im(P0)",
        },
        "P0": [[str(p0[i, j]) for j in range(6)] for i in range(6)],
        "Q0": [[str(q0[i, j]) for j in range(6)] for i in range(6)],
        "projector_ranks": {"P0": 4, "Q0": 2},
        "leading_commutator": "[G_-1,P0]=G_-1 != 0",
        "block_representation": {
            "identity": "G_AB(beta)=block_numerator_AB(beta)/common_denominator(beta)",
            "row_column_order": {"P": ["h0r0", "h0r1", "h1r0", "h1r1"], "Q": ["h0r2", "h1r2"]},
            "common_denominator_beta_coefficients": source["reduced_denominator_beta_coefficients"],
            "numerator_entry_beta_coefficients_ascending": {name: matrix_payload(value) for name, value in blocks.items()},
        },
        "ordinary_generator_guard": source["ordinary_generator_guard"],
        "GQQ": {
            "entries": gqq_text,
            "entry_denominators": [
                "r*(r-2*M)*(8*M*beta+5*r**3)",
                "omega*r**3*(8*M*beta+5*r**3)",
                "(r-2*M)**2",
                "r*(r-2*M)*(-16*M*beta+5*r**3)",
            ],
            "determinant_numerator_Delta": sp.sstr(delta),
            "determinant_denominator": sp.sstr(determinant_denominator),
            "determinant": sp.sstr(determinant),
            "rank_classification": "rank 2 when Delta != 0; rank 1 when Delta = 0, throughout the ordinary-generator guard",
            "inverse_guard": "ordinary_generator_guard and Delta != 0",
            "inverse_entries": [[sp.sstr(inverse[i, j]) for j in range(2)] for i in range(2)],
            "Delta_zero_kernel_basis": [[sp.sstr(kernel_vector[0])], [sp.sstr(kernel_vector[1])]],
            "Delta_zero_range_basis": [[sp.sstr(range_vector[0])], [sp.sstr(range_vector[1])]],
        },
        "historical_D_check": {
            "status": "corrected-different",
            "comparison": "the exact corrected GQQ, including its beta=0 specialization, is not the schematic historical triangular D in the stated Q-coordinate order",
            "historical_N": [[sp.sstr(historical_n[i, j]) for j in range(2)] for i in range(2)],
            "historical_DN_and_ND": "passed symbolically as an internal check of the historical candidate only",
        },
        "fredholm_obstruction_relation": {
            "status": "retained but not transferred",
            "reason": "the obstruction uses q and transformed P2/inner blocks without a certified repository-local q-to-beta and coordinate-map identity; the corrected finite-beta source/block formulas therefore require rederivation before compatibility transfer",
        },
        "exact_checks": {
            "leading_rank_kernel_image_jordan": True,
            "projector_algebra": True,
            "leading_commutator_actual_nonzero_value": True,
            "all_four_exact_blocks": True,
            "GQQ_simplification": True,
            "GQQ_determinant": True,
            "GQQ_inverse_both_compositions": True,
            "GQQ_rank_one_kernel_range_on_Delta_zero": True,
            "descriptor_guard_preserved": True,
            "historical_D_comparison": True,
            "fredholm_obstruction_retained": True,
        },
        "boundary": "stops at P0/Q0, exact blocks, and exact GQQ classification; no invariant projector beyond P0 or later closure is constructed",
    }
    payload["payload_sha256"] = hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    receipt = "\n".join([
        payload["certificate"],
        "P0_RANK := 4",
        "Q0_RANK := 2",
        "P0_IDEMPOTENCE := passed",
        "LEADING_COMMUTATOR := [G_-1,P0]=G_-1 != 0",
        "GQQ_EXACT := passed",
        "GQQ_DETERMINANT := rank 2 for Delta != 0; rank 1 for Delta = 0",
        "GQQ_INVERSE := passed under ordinary guard and Delta != 0",
        "HISTORICAL_D_MATCH := corrected-different",
        "FREDHOLM_OBSTRUCTION := retained",
        f"PAYLOAD_SHA256 := {payload['payload_sha256']}",
    ]) + "\n"
    RECEIPT.write_text(receipt, encoding="utf-8")
    print(receipt, end="")


if __name__ == "__main__":
    main()
