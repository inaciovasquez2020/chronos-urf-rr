#!/usr/bin/env python3
"""Certify the horizon-scaled logarithmic six-state exterior system.

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

Entrywise this is purely rational because every exponent 1-a_i+a_j is
integral.  The raw power scaling does not make the full six-state generator
analytic at x=0: exactly two simple-pole entries remain in the h1'' row.
This verifier classifies that residue exactly, proves that subtracting R/x
leaves a horizon-regular rational matrix, and checks that the physical
leading generalized-Frobenius scaled seed lies in ker(R).

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

    # Classify the exact horizon singular part.  The previous stronger claim
    # that every H_ij was regular is false: the exact system has two simple
    # poles, both in the h1'' row.  Preserve them as an explicit residue R.
    pole_positions: list[tuple[int, int]] = []
    pole_denominators: list[tuple[int, int, sp.Expr]] = []
    residue = sp.zeros(6, 6)
    nonzero_entry_count = 0
    for i in range(6):
        for j in range(6):
            value = simp(H[i, j])
            if value == 0:
                continue
            nonzero_entry_count += 1
            _num, den = sp.fraction(sp.together(value))
            if simp(den.subs(x, 0)) != 0:
                continue
            pole_positions.append((i, j))
            pole_denominators.append((i, j, sp.factor(den)))
            once = simp(x * value)
            _once_num, once_den = sp.fraction(sp.together(once))
            if simp(once_den.subs(x, 0)) == 0:
                raise AssertionError(f"scaled generator has pole order >1 at H[{i},{j}]")
            residue[i, j] = simp(once.subs(x, 0))
            if residue[i, j] == 0:
                raise AssertionError(f"purported simple-pole residue vanished at H[{i},{j}]")

    expected_pole_positions = [(5, 0), (5, 4)]
    if pole_positions != expected_pole_positions:
        raise AssertionError(
            f"scaled horizon pole support changed: got {pole_positions}, expected {expected_pole_positions}"
        )
    residue = matrix_simp(residue)
    if residue.rank() != 1:
        raise AssertionError(f"scaled horizon residue rank changed: {residue.rank()}")

    regular = matrix_simp(H - residue / x)
    regular_horizon_limit = sp.zeros(6, 6)
    regular_poles: list[tuple[int, int, sp.Expr]] = []
    for i in range(6):
        for j in range(6):
            value = simp(regular[i, j])
            if value == 0:
                continue
            _num, den = sp.fraction(sp.together(value))
            if simp(den.subs(x, 0)) == 0:
                regular_poles.append((i, j, sp.factor(den)))
                continue
            regular_horizon_limit[i, j] = simp(value.subs(x, 0))
    if regular_poles:
        raise AssertionError(f"residue-subtracted scaled generator retains horizon poles: {regular_poles}")
    regular_horizon_limit = matrix_simp(regular_horizon_limit)

    # The canonical ordinary n=0 physical vector is (h0, x*h1)=(1,2).
    # Differentiating the corresponding leading powers gives the exact scaled
    # six-state seed below.  The singular residue must annihilate it.
    physical_leading_scaled_seed = sp.Matrix([
        sp.Integer(1),
        sp.Rational(1, 2),
        sp.Rational(-1, 4),
        sp.Integer(2),
        sp.Integer(-1),
        sp.Rational(3, 2),
    ])
    residue_on_seed = matrix_simp(residue * physical_leading_scaled_seed)
    if any(value != 0 for value in residue_on_seed):
        raise AssertionError(f"physical leading scaled seed not in horizon residue kernel: {residue_on_seed}")

    # The four kinematic shift rows should become constant in log time after
    # the power scaling.  Pin them explicitly because they are useful for the
    # subsequent validated propagator.
    expected_shift_entries = ((0, 1), (1, 2), (3, 4), (4, 5))
    for i, j in expected_shift_entries:
        if simp(H[i, j] - 1) != 0:
            raise AssertionError(f"scaled kinematic shift H[{i},{j}] changed")

    zeta = sp.symbols("zeta")
    regular_horizon_characteristic = sp.factor(
        regular_horizon_limit.charpoly(zeta).as_expr()
    )

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
    print(f"HORIZON_SIMPLE_POLE_COUNT := {len(pole_positions)}")
    print("HORIZON_SIMPLE_POLE_POSITIONS := " + sp.sstr(pole_positions))
    print("HORIZON_SIMPLE_POLE_DENOMINATORS := " + sp.sstr(pole_denominators))
    print(f"HORIZON_RESIDUE_RANK := {residue.rank()}")
    print(f"HORIZON_RESIDUE_MATRIX := {matrix_text(residue)}")
    print("PHYSICAL_LEADING_SCALED_SEED := [1,1/2,-1/4,2,-1,3/2]")
    print("PHYSICAL_LEADING_SEED_RESIDUE := 0")
    print("REGULAR_REMAINDER := H_reg(x)=H(x)-R/x")
    print("REGULAR_REMAINDER_HORIZON_POLE_COUNT := 0")
    print(f"REGULAR_REMAINDER_HORIZON_LIMIT := {matrix_text(regular_horizon_limit)}")
    print(f"REGULAR_REMAINDER_HORIZON_CHARACTERISTIC := {sp.sstr(regular_horizon_characteristic)}")
    print("RAW_SCALED_EQUIVALENCE := Y=S(x)U and Y'=G(2+x)Y iff U_t=(R/x+H_reg(x))U for every x>0")
    print("CONDITIONING_ROUTE := preserve the rank-one residue constraint and construct a constraint-adapted blow-up before validated near-horizon propagation")
    print("BOUNDARY := exact scaled simple-pole/residue classification only; no constraint-adapted regular propagator, no validated propagation to r=4096, no Z_phys(4096) enclosure, no C_grow value/nonvanishing, and no global exceptional-mode closure claimed")


if __name__ == "__main__":
    main()
