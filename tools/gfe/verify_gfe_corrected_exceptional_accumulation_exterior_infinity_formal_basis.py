#!/usr/bin/env python3
"""Certify all-order pure inverse-r formal channels at physical infinity.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

Dependencies already enforced earlier in CI:
  * the exact exterior generator is rational and has the certified G_inf/G_1 data;
  * the refined oscillatory power blocks have spacing exactly one;
  * the G2 resonance audit certifies that both k=1 resonant obstructions vanish.

This verifier checks the remaining structural hypotheses for the formal
projected recurrence.  It proves that the exact generator is analytic in
s=1/r at s=0, constructs the constant refined eigen/power basis, removes the
cross-exponential 1/r terms by a near-identity gauge T(s)=I+s P1, and
classifies every positive-integer same-exponential power difference.

After the leading seed equation, the projected coefficient recurrence at
inverse-r order k has same-exponential denominator

    nu_j - k - nu_i.

Hence an obstruction can occur only when nu_j-nu_i is a positive integer k.
The exact classification below shows that the only such cases are the two
oscillatory high->low k=1 pairs, and the preceding G2 audit certifies both
compatibilities as zero.  Therefore the pure inverse-r formal recurrence is
solvable to all orders for all six channels.

No actual asymptotic-basis existence theorem and no projection of the physical
horizon solution onto these channels is claimed here.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_channels as ch
import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_g2_resonance as g2


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def main() -> None:
    r, G = ch.reconstruct_generator()

    # The exact rational generator must admit a full Taylor expansion in
    # s=1/r around infinity.  This is stronger than checking only G0,G1,G2.
    s = sp.symbols("s")
    analytic_entries = 0
    for value in G:
        value = simp(value)
        if value == 0:
            continue
        at_s = simp(value.subs(r, 1 / s))
        _num, den = sp.fraction(at_s)
        if simp(den.subs(s, 0)) == 0:
            raise AssertionError(
                f"generator entry is not analytic in s=1/r at s=0: {sp.sstr(value)}"
            )
        analytic_entries += 1

    G0 = ch.coefficient_at_power(G, r, 0)
    first_remainder = ch.ms(G - G0)
    G1 = ch.coefficient_at_power(first_remainder, r, -1)

    q = sp.sqrt(167)
    a = simp(sp.Rational(71, 1670) * q)
    block_data = [
        (sp.Rational(1, 4), [sp.Rational(3, 2)], ["EXP_GROWING"]),
        (-sp.Rational(1, 4), [sp.Rational(1, 2)], ["EXP_DECAYING"]),
        (
            sp.I * q / 20,
            [sp.I * a, 1 + sp.I * a],
            ["OSCILLATORY_PLUS_LOW", "OSCILLATORY_PLUS_HIGH"],
        ),
        (
            -sp.I * q / 20,
            [-sp.I * a, 1 - sp.I * a],
            ["OSCILLATORY_MINUS_LOW", "OSCILLATORY_MINUS_HIGH"],
        ),
    ]

    right_blocks: list[sp.Matrix] = []
    left_blocks: list[sp.Matrix] = []
    mus: list[sp.Expr] = []
    nus: list[sp.Expr] = []
    names: list[str] = []
    for mu, powers, block_names in block_data:
        R, L = g2.refined_block(G0, G1, mu, powers)
        right_blocks.append(R)
        left_blocks.append(L)
        mus.extend([mu] * len(powers))
        nus.extend(powers)
        names.extend(block_names)

    S = sp.Matrix.hstack(*right_blocks)
    Sinv = sp.Matrix.vstack(*left_blocks)
    if any(value != 0 for value in ms(Sinv * S - sp.eye(6))):
        raise AssertionError("refined constant basis lost duality")

    D0 = sp.diag(*mus)
    if any(value != 0 for value in ms(Sinv * G0 * S - D0)):
        raise AssertionError("refined constant basis no longer diagonalizes G_inf")

    B1 = ms(Sinv * G1 * S)

    # Remove only cross-exponential 1/r couplings.  Distinct exponential
    # rates give nonzero homological denominators mu_i-mu_j.
    P1 = sp.zeros(6, 6)
    cross_gap_count = 0
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            gap = simp(mus[i] - mus[j])
            if gap != 0:
                P1[i, j] = simp(-B1[i, j] / gap)
                cross_gap_count += 1
    P1 = ms(P1)

    N1 = ms(B1 + D0 * P1 - P1 * D0)
    expected_D1 = sp.diag(*nus)
    if any(value != 0 for value in ms(N1 - expected_D1)):
        raise AssertionError(
            f"first normal-form layer is not diagonal: {sp.sstr(N1)}"
        )

    T = sp.eye(6) + s * P1
    if simp(T.det().subs(s, 0) - 1) != 0:
        raise AssertionError("near-identity normal-form gauge is not invertible at infinity")

    # Classify all positive-integer power differences inside equal-mu blocks.
    # These are exactly the possible projected recurrence resonances k>=1.
    resonances: list[tuple[str, str, int]] = []
    for i in range(6):
        for j in range(6):
            if i == j or simp(mus[i] - mus[j]) != 0:
                continue
            diff = simp(nus[j] - nus[i])
            if diff.is_integer is True and diff.is_positive is True:
                resonances.append((names[j], names[i], int(diff)))

    expected_resonances = [
        ("OSCILLATORY_PLUS_HIGH", "OSCILLATORY_PLUS_LOW", 1),
        ("OSCILLATORY_MINUS_HIGH", "OSCILLATORY_MINUS_LOW", 1),
    ]
    if resonances != expected_resonances:
        raise AssertionError(f"same-mu positive-integer resonance set changed: {resonances}")

    # The immediately preceding exact G2 verifier certifies the compatibility
    # values for precisely these two k=1 equations:
    #
    #   OSCILLATORY_PLUS_K1_RESONANT_OBSTRUCTION  = 0
    #   OSCILLATORY_MINUS_K1_RESONANT_OBSTRUCTION = 0.
    #
    # Once those two equations are compatible, every later projected
    # denominator is nonzero because there are no further positive-integer
    # differences in the same exponential block.  The complement component
    # is solved uniquely at every order by (mu I-G_inf) on the direct sum of
    # all other eigenspaces.  This closes the formal induction.

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_FORMAL_BASIS_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("INFINITY_VARIABLE := s=1/r")
    print(f"EXACT_GENERATOR_NONZERO_ANALYTIC_ENTRIES := {analytic_entries}")
    print("GENERATOR_ANALYTIC_AT_INFINITY := every exact rational entry is analytic at s=0")
    print("REFINED_CONSTANT_BASIS := exact dual basis diagonalizing G_inf and the same-mu G_1 restrictions")
    print(f"EXPONENTIAL_RATES := {[sp.sstr(x) for x in mus]}")
    print(f"POWER_EXPONENTS := {[sp.sstr(x) for x in nus]}")
    print(f"CROSS_EXPONENTIAL_HOMOLOGICAL_DENOMINATORS_USED := {cross_gap_count}")
    print("FIRST_NORMAL_FORM_LAYER := diag(power exponents)/r")
    print("NEAR_IDENTITY_GAUGE := T(s)=I+s*P1 with det(T(0))=1")
    print(f"POSITIVE_INTEGER_SAME_EXPONENTIAL_RESONANCES := {resonances}")
    print("K1_RESONANCE_COMPATIBILITY_DEPENDENCY := preceding G2 audit certifies both exact obstruction values equal zero")
    print("HIGH_OSCILLATORY_RESONANT_NORMALIZATION := free low-channel coefficient at k=1 may be set to zero")
    print("POST_K1_PROJECTED_DENOMINATORS := nonzero for every integer k>=2 in every same-exponential block")
    print("COMPLEMENT_SOLVER := (mu*I-G_inf) is invertible on the direct sum of all other exponential eigenspaces")
    print("FORMAL_INVERSE_R_RECURRENCE := all-order solvable for each of the six channels")
    print("PURE_INVERSE_R_FORMAL_CHANNEL_COUNT := 6")
    print("FORMAL_INFINITY_BASIS := six independent exp(mu*r)*r^nu pure inverse-r formal series")
    print("BOUNDARY := formal asymptotic basis only; no actual asymptotic-solution theorem and no physical horizon-solution channel projection claimed")


if __name__ == "__main__":
    main()
