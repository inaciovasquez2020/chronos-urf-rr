#!/usr/bin/env python3
"""Certify a horizon-regular scaled logarithmic six-state exterior system.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The reconstructed physical state is

    Y=(h0,h0',h0'',h1,h1',h1'')^T

and the exact exterior descriptor gives Y'=G(r)Y for every r>2.  Near the
horizon set x=r-2 and factor the powers dictated by the reconstructed
x^(1/2) generalized-Frobenius branch,

    Y_i = x^(a_i) U_i,
    a=(1/2,-1/2,-3/2,-1/2,-3/2,-5/2).

With logarithmic time t=log(x), the scaled state obeys

    dU/dt = H(x) U,
    H(x)=x*S(x)^(-1)*G(2+x)*S(x)-diag(a).

Entrywise this is purely rational because every exponent
1-a_i+a_j is integral.  This verifier constructs H exactly and certifies that
all apparent x=0 poles cancel, so H extends analytically to the horizon.

This is a conditioning/structure certificate only.  It does not numerically
propagate the startup enclosure and does not evaluate C_grow.
"""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_continuation as exterior

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


def matrix_text(matrix: sp.Matrix) -> str:
    return sp.sstr([
        [simp(matrix[i, j]) for j in range(matrix.cols)]
        for i in range(matrix.rows)
    ])


def build_generator() -> tuple[sp.Symbol, sp.Matrix]:
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

    # Reuse the exact triangular derivative-block construction audited by the
    # infinity-symbol verifier.  Rows 0,1,3,4 are elementary derivative shifts.
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

    a = simp(E[4, 2])
    c = simp(E[5, 2])
    d = simp(E[5, 5])
    if simp(E[4, 5]) != 0:
        raise AssertionError("descriptor derivative block lost lower-triangular form")
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
        raise AssertionError("exact descriptor solve E*G=A failed")
    return r, G


def main() -> None:
    # Lock the immediate exterior-continuation dependency on the same artifact.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exterior.main()
    exterior_log = buffer.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_CONTINUATION_CERTIFIED",
        "DESCRIPTOR_INVERTIBILITY := certified for every real r>2",
        "PHYSICAL_EXTERIOR_CONTINUATION := unique to every finite r>2",
    ]:
        if token not in exterior_log:
            raise AssertionError("exterior-continuation dependency changed: " + token)

    r, G = build_generator()
    x = sp.symbols("x", nonnegative=True)
    powers = [
        sp.Rational(1, 2),
        sp.Rational(-1, 2),
        sp.Rational(-3, 2),
        sp.Rational(-1, 2),
        sp.Rational(-3, 2),
        sp.Rational(-5, 2),
    ]

    H = sp.zeros(6, 6)
    exponent_matrix: list[list[int | None]] = []
    noninteger: list[tuple[int, int, sp.Expr]] = []
    negative_exponents: list[tuple[int, int, int]] = []
    for i in range(6):
        row_exponents: list[int | None] = []
        for j in range(6):
            if G[i, j] == 0:
                row_exponents.append(None)
                continue
            exponent = simp(1 - powers[i] + powers[j])
            if not bool(exponent.is_integer):
                noninteger.append((i, j, exponent))
                row_exponents.append(None)
                continue
            exponent_int = int(exponent)
            row_exponents.append(exponent_int)
            if exponent_int < 0:
                negative_exponents.append((i, j, exponent_int))
            H[i, j] = simp(x**exponent_int * G[i, j].subs(r, x + 2))
        exponent_matrix.append(row_exponents)
    if noninteger:
        raise AssertionError(f"noninteger scaled-generator exponents: {noninteger}")

    for i in range(6):
        H[i, i] = simp(H[i, i] - powers[i])
    H = matrix_simp(H)

    # Exact horizon regularity: every simplified rational denominator is
    # nonzero at x=0.  This is the key cancellation certificate.
    horizon_poles: list[tuple[int, int, sp.Expr]] = []
    horizon_limits = sp.zeros(6, 6)
    nonzero_entry_count = 0
    for i in range(6):
        for j in range(6):
            value = simp(H[i, j])
            if value == 0:
                continue
            nonzero_entry_count += 1
            _num, den = sp.fraction(sp.together(value))
            den0 = simp(den.subs(x, 0))
            if den0 == 0:
                horizon_poles.append((i, j, sp.factor(den)))
                continue
            horizon_limits[i, j] = simp(value.subs(x, 0))
    if horizon_poles:
        raise AssertionError(f"scaled logarithmic generator retains horizon poles: {horizon_poles}")
    horizon_limits = matrix_simp(horizon_limits)

    # The four kinematic shift rows should become constant in log time after
    # the power scaling.  Pin them explicitly because they are useful for the
    # subsequent validated propagator.
    expected_shift_entries = ((0, 1), (1, 2), (3, 4), (4, 5))
    for i, j in expected_shift_entries:
        if simp(H[i, j] - 1) != 0:
            raise AssertionError(f"scaled kinematic shift H[{i},{j}] changed")

    zeta = sp.symbols("zeta")
    horizon_characteristic = sp.factor(horizon_limits.charpoly(zeta).as_expr())

    def exponent_text(value: int | None) -> str:
        return "-inf" if value is None else str(value)

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_HORIZON_SCALED_LOG_SYSTEM_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("RAW_STATE := Y=(h0,h0',h0'',h1,h1',h1'')")
    print("HORIZON_VARIABLE := x=r-2")
    print("LOG_TIME := t=log(x); therefore d/dt=x*d/dx")
    print("RAW_POWER_VECTOR := [1/2,-1/2,-3/2,-1/2,-3/2,-5/2]")
    print("SCALED_STATE := U_i=x^(-a_i)*Y_i")
    print("SCALED_LOG_GENERATOR := H_ij=x^(1-a_i+a_j)*G_ij(2+x)-a_i*delta_ij")
    print("NONINTEGER_ENTRY_EXPONENTS := none")
    print("NEGATIVE_PRECANCELLATION_ENTRY_EXPONENTS := " + sp.sstr(negative_exponents))
    print("ENTRY_EXPONENT_MATRIX := [" + "; ".join(
        "[" + ",".join(exponent_text(v) for v in row) + "]" for row in exponent_matrix
    ) + "]")
    print(f"SCALED_LOG_GENERATOR_NONZERO_ENTRIES := {nonzero_entry_count}")
    print("HORIZON_POLE_COUNT := 0")
    print("HORIZON_REGULARITY := every simplified rational H_ij has denominator nonzero at x=0")
    print(f"HORIZON_LIMIT_H0 := {matrix_text(horizon_limits)}")
    print(f"HORIZON_LIMIT_CHARACTERISTIC := {sp.sstr(horizon_characteristic)}")
    print("RAW_SCALED_EQUIVALENCE := Y=S(x)U and Y'=G(2+x)Y iff U_t=H(x)U for every x>0")
    print("CONDITIONING_ROUTE := propagate U in logarithmic x near the horizon, then map to a regular exterior representation away from x=0")
    print("BOUNDARY := scaled logarithmic system only; no validated propagation to r=4096, no Z_phys(4096) enclosure, no C_grow value/nonvanishing, and no global exceptional-mode closure claimed")


if __name__ == "__main__":
    main()
