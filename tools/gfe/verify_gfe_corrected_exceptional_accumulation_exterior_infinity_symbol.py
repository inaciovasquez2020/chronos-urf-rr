#!/usr/bin/env python3
"""Audit the exact physical-space infinity symbol in the accumulation sector.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The preceding gates construct an actual horizon solution and continue it
uniquely to every finite r>2.  This verifier reads the same authoritative
six-state descriptor

    E(r) Y'(r) = A(r) Y(r),

forms the guarded ordinary generator G=E^{-1}A by the descriptor's exact
lower-triangular derivative block, and classifies every entry by its Laurent
power at r=infinity.  If the generator is asymptotically constant, it also
exports the exact limiting matrix and its characteristic polynomial.

This is deliberately a symbol audit only.  It does not yet prove an
asymptotic basis theorem, identify the physical solution's infinity-channel
coefficients, or impose an outgoing/decaying boundary condition.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def matrix_simp(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def parse_matrix(raw: list[list[str]], locals_: dict[str, sp.Expr]) -> sp.Matrix:
    return sp.Matrix([
        [sp.sympify(entry, locals=locals_) for entry in row]
        for row in raw
    ])


def rational_infinity_data(value: sp.Expr, r: sp.Symbol) -> tuple[int | None, sp.Expr]:
    """Return (power, coefficient) for value ~ coefficient*r**power."""
    value = simp(value)
    if value == 0:
        return None, sp.Integer(0)
    numerator, denominator = sp.fraction(value)
    numerator_poly = sp.Poly(numerator, r, domain=sp.QQ_I)
    denominator_poly = sp.Poly(denominator, r, domain=sp.QQ_I)
    power = numerator_poly.degree() - denominator_poly.degree()
    coefficient = simp(numerator_poly.LC() / denominator_poly.LC())
    return int(power), coefficient


def power_text(power: int | None) -> str:
    return "-inf" if power is None else str(power)


def matrix_text(matrix: sp.Matrix) -> str:
    return sp.sstr([[simp(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)])


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("state_dimension") != 6:
        raise AssertionError(f"descriptor state dimension changed: {data.get('state_dimension')}")

    M, beta, lam, omega, r = sp.symbols("M beta lam omega r")
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "lambda": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
    }
    specialization = {
        M: sp.Integer(1),
        beta: sp.Rational(5, 2),
        lam: sp.Integer(6),
        omega: sp.I / 4,
    }

    E = matrix_simp(parse_matrix(data["descriptor_E"], locals_).subs(specialization))
    A = matrix_simp(parse_matrix(data["descriptor_A"], locals_).subs(specialization))
    if E.shape != (6, 6) or A.shape != (6, 6):
        raise AssertionError(f"descriptor shape changed: E={E.shape}, A={A.shape}")

    # Pin the exact descriptor staircase used by the generator derivation.
    expected_shift_rows = ((0, 0, 1), (1, 1, 2), (2, 3, 4), (3, 4, 5))
    for equation_row, derivative_col, state_col in expected_shift_rows:
        if simp(E[equation_row, derivative_col] - 1) != 0:
            raise AssertionError(f"descriptor shift E[{equation_row},{derivative_col}] changed")
        if sum(E[equation_row, j] != 0 for j in range(6)) != 1:
            raise AssertionError(f"descriptor shift row {equation_row} is no longer elementary")
        if simp(A[equation_row, state_col] - 1) != 0:
            raise AssertionError(f"descriptor shift A[{equation_row},{state_col}] changed")
        if sum(A[equation_row, j] != 0 for j in range(6)) != 1:
            raise AssertionError(f"generator shift row {equation_row} is no longer elementary")

    # The nontrivial derivative block is B=[[a,0],[c,d]] in equation rows
    # (4,5) and derivative columns (2,5).  Construct G without a dense inverse.
    a = simp(E[4, 2])
    upper_right = simp(E[4, 5])
    c = simp(E[5, 2])
    d = simp(E[5, 5])
    if upper_right != 0:
        raise AssertionError(f"descriptor derivative block lost triangular form: {upper_right}")
    if a == 0 or d == 0:
        raise AssertionError("descriptor derivative pivot vanished identically")

    G = sp.zeros(6, 6)
    for generator_row, equation_row in ((0, 0), (1, 1), (3, 2), (4, 3)):
        for j in range(6):
            G[generator_row, j] = A[equation_row, j]
    for j in range(6):
        G[2, j] = simp(A[4, j] / a)
        G[5, j] = simp((a * A[5, j] - c * A[4, j]) / (a * d))
    G = matrix_simp(G)

    residual = matrix_simp(E * G - A)
    if any(value != 0 for value in residual):
        raise AssertionError(f"exact descriptor solve failed: {residual.tolist()}")

    powers: list[list[int | None]] = []
    leading_coefficients: list[list[sp.Expr]] = []
    finite_powers: list[int] = []
    for i in range(6):
        power_row: list[int | None] = []
        coefficient_row: list[sp.Expr] = []
        for j in range(6):
            power, coefficient = rational_infinity_data(G[i, j], r)
            power_row.append(power)
            coefficient_row.append(coefficient)
            if power is not None:
                finite_powers.append(power)
        powers.append(power_row)
        leading_coefficients.append(coefficient_row)
    if not finite_powers:
        raise AssertionError("ordinary generator is identically zero")
    max_power = max(finite_powers)

    leading_matrix = sp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            if powers[i][j] == max_power:
                leading_matrix[i, j] = leading_coefficients[i][j]
    leading_matrix = matrix_simp(leading_matrix)

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_SYMBOL_AUDIT")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("DEPENDENCY := actual reconstructed branch continues uniquely to every finite r>2")
    print("PHYSICAL_SPACE_STATE := Y=(h0,h0',h0'',h1,h1',h1'')")
    print("ORDINARY_GENERATOR := G(r)=E(r)^(-1)A(r), constructed exactly from the triangular descriptor block")
    print("EXACT_DESCRIPTOR_SOLVE := E*G-A = 0")
    print("GENERATOR_INFINITY_POWER_MATRIX := [" + "; ".join(
        "[" + ",".join(power_text(value) for value in row) + "]" for row in powers
    ) + "]")
    print(f"MAX_GENERATOR_INFINITY_POWER := {max_power}")
    print(f"MAX_POWER_LEADING_MATRIX := {matrix_text(leading_matrix)}")

    if max_power <= 0:
        G_infinity = sp.zeros(6, 6)
        for i in range(6):
            for j in range(6):
                if powers[i][j] == 0:
                    G_infinity[i, j] = leading_coefficients[i][j]
        G_infinity = matrix_simp(G_infinity)

        remainder_max = None
        remainder = matrix_simp(G - G_infinity)
        remainder_powers: list[int] = []
        for value in remainder:
            power, _coefficient = rational_infinity_data(value, r)
            if power is not None:
                remainder_powers.append(power)
        if remainder_powers:
            remainder_max = max(remainder_powers)
            if remainder_max >= 0:
                raise AssertionError(f"constant infinity subtraction left nondecaying power {remainder_max}")

        mu = sp.symbols("mu")
        characteristic = sp.factor(G_infinity.charpoly(mu).as_expr())
        print("INFINITY_GENERATOR_CLASS := asymptotically constant")
        print(f"G_INFINITY := {matrix_text(G_infinity)}")
        print(f"G_MINUS_G_INFINITY_MAX_POWER := {remainder_max if remainder_max is not None else '-inf'}")
        print(f"INFINITY_CHARACTERISTIC_POLYNOMIAL := {sp.sstr(characteristic)}")
        print("BOUNDARY := constant infinity symbol only; asymptotic-basis existence, channel powers, and physical projection remain unproved")
    else:
        print("INFINITY_GENERATOR_CLASS := polynomially growing; constant-symbol reduction is invalid without a further exact shearing/Newton analysis")
        print("BOUNDARY := leading physical-space infinity power exposed only; asymptotic-basis existence and physical channel projection remain unproved")


if __name__ == "__main__":
    main()
