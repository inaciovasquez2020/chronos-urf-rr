#!/usr/bin/env python3
"""Certify the exact first two asymptotic layers of the physical infinity channels.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The preceding infinity-symbol audit proves that the exact physical six-state
system has

    Y' = G(r) Y,
    G(r) = G_inf + O(1/r),

with characteristic polynomial

    (4 mu - 1)(4 mu + 1)(400 mu^2 + 167)^2 / 2560000.

This verifier reconstructs G(r) from the same authoritative descriptor,
certifies the exact refinement

    G(r) = G_inf + G_1/r + O(1/r^2),

proves G_inf is semisimple, and compresses G_1 to each eigenspace of G_inf.
Those compressed matrices are the exact algebraic power-law data associated
with the exponential rates.  No asymptotic-basis existence theorem and no
projection of the physical horizon solution onto these channels is claimed.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def parse_matrix(raw: list[list[str]], locals_: dict[str, sp.Expr]) -> sp.Matrix:
    return sp.Matrix([
        [sp.sympify(entry, locals=locals_) for entry in row]
        for row in raw
    ])


def infinity_power_and_coefficient(value: sp.Expr, r: sp.Symbol) -> tuple[int | None, sp.Expr]:
    value = simp(value)
    if value == 0:
        return None, sp.Integer(0)
    numerator, denominator = sp.fraction(value)
    pn = sp.Poly(numerator, r, domain=sp.QQ_I)
    pd = sp.Poly(denominator, r, domain=sp.QQ_I)
    return int(pn.degree() - pd.degree()), simp(pn.LC() / pd.LC())


def max_infinity_power(matrix: sp.Matrix, r: sp.Symbol) -> int | None:
    powers: list[int] = []
    for value in matrix:
        power, _ = infinity_power_and_coefficient(value, r)
        if power is not None:
            powers.append(power)
    return max(powers) if powers else None


def coefficient_at_power(matrix: sp.Matrix, r: sp.Symbol, target: int) -> sp.Matrix:
    out = sp.zeros(matrix.rows, matrix.cols)
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            power, coeff = infinity_power_and_coefficient(matrix[i, j], r)
            if power == target:
                out[i, j] = coeff
    return ms(out)


def reconstruct_generator() -> tuple[sp.Symbol, sp.Matrix]:
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
    E = ms(parse_matrix(data["descriptor_E"], locals_).subs(specialization))
    A = ms(parse_matrix(data["descriptor_A"], locals_).subs(specialization))

    a = simp(E[4, 2])
    if simp(E[4, 5]) != 0:
        raise AssertionError("descriptor derivative block lost lower-triangular form")
    c = simp(E[5, 2])
    d = simp(E[5, 5])
    if a == 0 or d == 0:
        raise AssertionError("descriptor derivative pivot vanished identically")

    G = sp.zeros(6, 6)
    for generator_row, equation_row in ((0, 0), (1, 1), (3, 2), (4, 3)):
        for j in range(6):
            G[generator_row, j] = A[equation_row, j]
    for j in range(6):
        G[2, j] = simp(A[4, j] / a)
        G[5, j] = simp((a * A[5, j] - c * A[4, j]) / (a * d))
    G = ms(G)
    if any(value != 0 for value in ms(E * G - A)):
        raise AssertionError("exact descriptor solve E*G=A failed")
    return r, G


def dual_restriction(G0: sp.Matrix, G1: sp.Matrix, eigenvalue: sp.Expr, multiplicity: int) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    right_vectors = (G0 - eigenvalue * sp.eye(6)).nullspace()
    left_vectors = (G0.T - eigenvalue * sp.eye(6)).nullspace()
    if len(right_vectors) != multiplicity or len(left_vectors) != multiplicity:
        raise AssertionError(
            f"eigenspace dimension changed at {sp.sstr(eigenvalue)}: "
            f"right={len(right_vectors)}, left={len(left_vectors)}, expected={multiplicity}"
        )
    R = sp.Matrix.hstack(*right_vectors)
    W = sp.Matrix.hstack(*left_vectors).T
    pairing = ms(W * R)
    if simp(pairing.det()) == 0:
        raise AssertionError(f"left/right eigenbasis pairing singular at {sp.sstr(eigenvalue)}")
    L = ms(pairing.inv() * W)
    if any(value != 0 for value in ms(L * R - sp.eye(multiplicity))):
        raise AssertionError("dual eigenbasis normalization failed")
    H = ms(L * G1 * R)
    return R, L, H


def matrix_text(matrix: sp.Matrix) -> str:
    return sp.sstr([[simp(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)])


def main() -> None:
    r, G = reconstruct_generator()

    G0 = coefficient_at_power(G, r, 0)
    expected_G0 = sp.Matrix([
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, -sp.Rational(167, 400), 0, sp.Rational(167, 1600), 0, sp.Rational(1, 4)],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [sp.Rational(167, 1600), 0, sp.Rational(1, 4), 0, -sp.Rational(167, 400), 0],
    ])
    if any(value != 0 for value in ms(G0 - expected_G0)):
        raise AssertionError("G_infinity changed from preceding exact certificate")

    mu = sp.symbols("mu")
    expected_charpoly = sp.factor(
        (4 * mu - 1) * (4 * mu + 1) * (400 * mu**2 + 167) ** 2
        / sp.Integer(2560000)
    )
    charpoly = sp.factor(G0.charpoly(mu).as_expr())
    if simp(charpoly - expected_charpoly) != 0:
        raise AssertionError(f"infinity characteristic polynomial changed: {charpoly}")

    first_remainder = ms(G - G0)
    if max_infinity_power(first_remainder, r) != -1:
        raise AssertionError("first infinity correction is no longer exactly order 1/r")
    G1 = coefficient_at_power(first_remainder, r, -1)
    second_remainder = ms(G - G0 - G1 / r)
    second_power = max_infinity_power(second_remainder, r)
    if second_power is not None and second_power > -2:
        raise AssertionError(f"remainder after G1/r is not O(r^-2): power={second_power}")

    q = sp.sqrt(167)
    spectral_data = [
        (sp.Rational(1, 4), 1, "EXP_GROWING"),
        (-sp.Rational(1, 4), 1, "EXP_DECAYING"),
        (sp.I * q / 20, 2, "OSCILLATORY_PLUS"),
        (-sp.I * q / 20, 2, "OSCILLATORY_MINUS"),
    ]

    restrictions: list[tuple[sp.Expr, int, str, sp.Matrix, sp.Expr, int]] = []
    total_dimension = 0
    for eigenvalue, multiplicity, label in spectral_data:
        _R, _L, H = dual_restriction(G0, G1, eigenvalue, multiplicity)
        total_dimension += multiplicity
        nu = sp.symbols("nu")
        h_charpoly = sp.factor(H.charpoly(nu).as_expr())
        # Count geometric dimensions of every algebraic power root when SymPy
        # can factor them explicitly.  The discriminant check below handles
        # the 2x2 blocks without requiring numerical roots.
        if multiplicity == 1:
            h_diag_dim = 1
        else:
            discr = simp(sp.discriminant(sp.Poly(h_charpoly, nu), nu))
            if discr != 0:
                h_diag_dim = multiplicity
            else:
                root = simp(-H.trace() / 2)
                h_diag_dim = len((H - root * sp.eye(2)).nullspace())
                if h_diag_dim != multiplicity:
                    raise AssertionError(
                        f"1/r restriction has a nontrivial Jordan block in {label}: {matrix_text(H)}"
                    )
        restrictions.append((eigenvalue, multiplicity, label, H, h_charpoly, h_diag_dim))

    if total_dimension != 6:
        raise AssertionError(f"infinity eigenspaces do not span the six-state system: {total_dimension}")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_CHANNEL_DATA_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("PHYSICAL_SPACE_STATE := Y=(h0,h0',h0'',h1,h1',h1'')")
    print("ASYMPTOTIC_GENERATOR := G(r)=G_inf+G_1/r+O(r^-2)")
    print(f"G_INFINITY := {matrix_text(G0)}")
    print(f"G_1 := {matrix_text(G1)}")
    print(f"POST_G1_REMAINDER_MAX_POWER := {second_power if second_power is not None else '-inf'}")
    print("G_INFINITY_CHARACTERISTIC := (4*mu-1)*(4*mu+1)*(400*mu^2+167)^2/2560000")
    print("G_INFINITY_SEMISIMPLE := True; eigenspace dimensions 1+1+2+2=6")
    for eigenvalue, multiplicity, label, H, h_charpoly, h_diag_dim in restrictions:
        print(f"{label}_EXPONENTIAL_RATE := {sp.sstr(eigenvalue)}")
        print(f"{label}_MULTIPLICITY := {multiplicity}")
        print(f"{label}_G1_RESTRICTION := {matrix_text(H)}")
        print(f"{label}_POWER_CHARACTERISTIC := {sp.sstr(h_charpoly)}")
        print(f"{label}_POWER_BLOCK_SEMISIMPLE_DIMENSION := {h_diag_dim}")
    print("FORMAL_CHANNEL_TEMPLATE := exp(mu*r)*r^nu times an inverse-r asymptotic series, with nu from the corresponding power characteristic")
    print("BOUNDARY := exact exponential and first power-law channel data only; asymptotic-basis existence and physical horizon-solution projection remain unproved")


if __name__ == "__main__":
    main()
