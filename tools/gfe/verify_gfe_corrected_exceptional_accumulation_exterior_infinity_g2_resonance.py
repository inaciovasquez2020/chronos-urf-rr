#!/usr/bin/env python3
"""Audit the first integer-power resonance in the physical infinity normal form.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The preceding channel-data verifier certifies

    Y' = (G_inf + G_1/r + O(r^-2)) Y,

with semisimple G_inf and two oscillatory G_inf eigenspaces whose G_1 power
exponents differ by exactly one.  That integer difference creates the only
possible first inverse-r resonance inside either repeated exponential block.

This verifier refines the constant eigenbasis so that the projected G_1 action
is diagonal, removes all 1/r couplings between distinct exponential rates by
an exact near-identity transformation, reconstructs the resulting 1/r^2
coefficient, and exposes the two k=1 resonant entries.

This is a normal-form/resonance audit only.  It does not claim an actual
asymptotic basis or project the physical horizon solution onto infinity
channels.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_channels as ch


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def infinity_power_and_coefficient(value: sp.Expr, r: sp.Symbol) -> tuple[int | None, sp.Expr]:
    value = simp(value)
    if value == 0:
        return None, sp.Integer(0)
    numerator, denominator = sp.fraction(value)
    pn = sp.Poly(numerator, r, domain="EX")
    pd = sp.Poly(denominator, r, domain="EX")
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


def refined_block(
    G0: sp.Matrix,
    G1: sp.Matrix,
    eigenvalue: sp.Expr,
    powers: list[sp.Expr],
) -> tuple[sp.Matrix, sp.Matrix]:
    multiplicity = len(powers)
    R, L, H = ch.dual_restriction(G0, G1, eigenvalue, multiplicity)

    if multiplicity == 1:
        if simp(H[0, 0] - powers[0]) != 0:
            raise AssertionError(
                f"1/r power changed at mu={sp.sstr(eigenvalue)}: {sp.sstr(H[0, 0])}"
            )
        return ms(R), ms(L)

    vectors: list[sp.Matrix] = []
    for nu in powers:
        null = (H - nu * sp.eye(multiplicity)).nullspace()
        if len(null) != 1:
            raise AssertionError(
                f"expected simple G1 power eigenvector at mu={sp.sstr(eigenvalue)}, nu={sp.sstr(nu)}"
            )
        vectors.append(null[0])
    V = sp.Matrix.hstack(*vectors)
    if simp(V.det()) == 0:
        raise AssertionError("refined G1 power eigenbasis is singular")

    R2 = ms(R * V)
    L2 = ms(V.inv() * L)
    if any(value != 0 for value in ms(L2 * R2 - sp.eye(multiplicity))):
        raise AssertionError("refined dual basis normalization failed")
    projected = ms(L2 * G1 * R2)
    if any(value != 0 for value in ms(projected - sp.diag(*powers))):
        raise AssertionError(
            f"refined G1 block is not diagonal: {sp.sstr(projected)}"
        )
    return R2, L2


def matrix_text(matrix: sp.Matrix) -> str:
    return sp.sstr([[simp(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)])


def main() -> None:
    r, G = ch.reconstruct_generator()
    G0 = ch.coefficient_at_power(G, r, 0)
    first_remainder = ch.ms(G - G0)
    G1 = ch.coefficient_at_power(first_remainder, r, -1)

    q = sp.sqrt(167)
    a = simp(sp.Rational(71, 1670) * q)

    block_data = [
        (sp.Rational(1, 4), [sp.Rational(3, 2)], "EXP_GROWING"),
        (-sp.Rational(1, 4), [sp.Rational(1, 2)], "EXP_DECAYING"),
        (sp.I * q / 20, [sp.I * a, 1 + sp.I * a], "OSCILLATORY_PLUS"),
        (-sp.I * q / 20, [-sp.I * a, 1 - sp.I * a], "OSCILLATORY_MINUS"),
    ]

    right_blocks: list[sp.Matrix] = []
    left_blocks: list[sp.Matrix] = []
    mus: list[sp.Expr] = []
    nus: list[sp.Expr] = []
    labels: list[str] = []
    for mu, powers, label in block_data:
        R, L = refined_block(G0, G1, mu, powers)
        right_blocks.append(R)
        left_blocks.append(L)
        mus.extend([mu] * len(powers))
        nus.extend(powers)
        labels.extend([label] * len(powers))

    S = sp.Matrix.hstack(*right_blocks)
    Sinv = sp.Matrix.vstack(*left_blocks)
    if any(value != 0 for value in ms(Sinv * S - sp.eye(6))):
        raise AssertionError("global refined left/right basis is not dual")

    D0 = sp.diag(*mus)
    if any(value != 0 for value in ms(Sinv * G0 * S - D0)):
        raise AssertionError("refined basis does not diagonalize G_inf")

    B = ms(Sinv * G * S)
    B1 = coefficient_at_power(ms(B - D0), r, -1)
    rem2 = ms(B - D0 - B1 / r)
    if max_infinity_power(rem2, r) != -2:
        raise AssertionError("refined generator no longer has an exact 1/r^2 next layer")
    B2 = coefficient_at_power(rem2, r, -2)

    # Remove all 1/r couplings across distinct exponential rates.  With
    # Z=(I+P1/r)W, the 1/r coefficient is B1+[D0,P1].
    P1 = sp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            if i != j and simp(mus[i] - mus[j]) != 0:
                P1[i, j] = simp(-B1[i, j] / (mus[i] - mus[j]))
    P1 = ms(P1)

    N1 = ms(B1 + D0 * P1 - P1 * D0)
    expected_N1 = sp.diag(*nus)
    if any(value != 0 for value in ms(N1 - expected_N1)):
        raise AssertionError(
            f"first normal-form coefficient is not diagonal: {matrix_text(N1)}"
        )

    # Exact coefficient through 1/r^2 for Z=(I+P1/r)W:
    # T^{-1}BT - T^{-1}T', with T=I+P1/r.
    N2 = ms(
        B2
        + B1 * P1
        - P1 * B1
        - P1 * D0 * P1
        + P1 * P1 * D0
        + P1
    )

    # Index order is growing, decaying, plus-low, plus-high, minus-low,
    # minus-high.  For a column j, the k=1 same-mu recurrence denominator is
    # nu_j - 1 - nu_i.  Hence the only integer-power resonances are high->low
    # in the two oscillatory blocks because nu_high-nu_low=1 exactly.
    if simp(nus[3] - nus[2] - 1) != 0 or simp(nus[5] - nus[4] - 1) != 0:
        raise AssertionError("oscillatory power spacing is no longer exactly one")

    plus_obstruction = simp(N2[2, 3])
    minus_obstruction = simp(N2[4, 5])
    plus_zero = plus_obstruction == 0
    minus_zero = minus_obstruction == 0

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_G2_RESONANCE_AUDIT")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("REFINED_INFINITY_NORMAL_FORM := D0 + D1/r + N2/r^2 + O(r^-3) up to the certified displayed layers")
    print(f"D0_EXPONENTIAL_RATES := {[sp.sstr(x) for x in mus]}")
    print(f"D1_POWER_EXPONENTS := {[sp.sstr(x) for x in nus]}")
    print("OSCILLATORY_PLUS_POWER_SPACING := 1")
    print("OSCILLATORY_MINUS_POWER_SPACING := 1")
    print(f"CROSS_EXPONENTIAL_P1 := {matrix_text(P1)}")
    print(f"NORMAL_FORM_N2 := {matrix_text(N2)}")
    print(f"OSCILLATORY_PLUS_K1_RESONANT_OBSTRUCTION := {sp.sstr(plus_obstruction)}")
    print(f"OSCILLATORY_MINUS_K1_RESONANT_OBSTRUCTION := {sp.sstr(minus_obstruction)}")
    print(f"OSCILLATORY_PLUS_K1_RESONANCE_VANISHES := {plus_zero}")
    print(f"OSCILLATORY_MINUS_K1_RESONANCE_VANISHES := {minus_zero}")
    if plus_zero and minus_zero:
        print("PURE_INVERSE_R_FORMAL_CHANNELS := first and only positive-integer same-exponential power resonance is unobstructed")
    else:
        print("PURE_INVERSE_R_FORMAL_CHANNELS := obstructed at k=1 in at least one oscillatory block; logarithmic/resonant refinement required")
    print("BOUNDARY := first resonant infinity normal-form data only; no actual asymptotic-basis existence theorem and no physical horizon-solution channel projection claimed")


if __name__ == "__main__":
    main()
