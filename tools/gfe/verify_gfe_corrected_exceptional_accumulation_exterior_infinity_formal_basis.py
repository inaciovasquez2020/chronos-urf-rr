#!/usr/bin/env python3
"""Certify all-order pure inverse-r formal channels at physical infinity.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

Dependencies already enforced earlier in CI:
  * the exact exterior generator is rational and has the certified G_inf/G_1 data;
  * the refined oscillatory power blocks have spacing exactly one;
  * the G2 resonance audit certifies that both k=1 resonant obstructions vanish.

This verifier independently rechecks those two G2 obstruction values, then
checks the remaining structural hypotheses for the formal projected recurrence.
It proves that the exact generator is analytic in s=1/r at s=0, constructs the
constant refined eigen/power basis, removes the cross-exponential 1/r terms,
and diagonalizes the entire 1/r^2 layer by exact near-identity homological
transforms.  The resulting analytic normal form is

    D0 + D1/r + D2/r^2 + O(r^-3),

with D0,D1,D2 diagonal.

After the leading seed equation, the projected coefficient recurrence at
inverse-r order k has same-exponential denominator

    nu_j - k - nu_i.

Hence an obstruction can occur only when nu_j-nu_i is a positive integer k.
The exact classification below shows that the only such cases are the two
oscillatory high->low k=1 pairs, and this verifier recomputes both exact
compatibility values as zero. Therefore the pure inverse-r formal recurrence
is solvable to all orders for all six channels.

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


def off_diagonal_nonzero(matrix: sp.Matrix) -> list[tuple[int, int, sp.Expr]]:
    out: list[tuple[int, int, sp.Expr]] = []
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if i != j:
                value = simp(matrix[i, j])
                if value != 0:
                    out.append((i, j, value))
    return out


def main() -> None:
    r, G = ch.reconstruct_generator()

    # The exact rational generator must admit a full Taylor expansion in
    # s=1/r around infinity. This is stronger than checking only G0,G1,G2.
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

    B = ms(Sinv * G * S)
    B1 = g2.coefficient_at_power(ms(B - D0), r, -1)

    # Remove only cross-exponential 1/r couplings. Distinct exponential
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
    D1 = sp.diag(*nus)
    if any(value != 0 for value in ms(N1 - D1)):
        raise AssertionError(
            f"first normal-form layer is not diagonal: {sp.sstr(N1)}"
        )

    T1 = sp.eye(6) + s * P1
    if simp(T1.det().subs(s, 0) - 1) != 0:
        raise AssertionError("first near-identity normal-form gauge is not invertible at infinity")

    # Recompute the exact second normal-form layer and the two k=1 resonant
    # compatibility values. This makes the all-order gate self-contained.
    rem2 = ms(B - D0 - B1 / r)
    if g2.max_infinity_power(rem2, r) != -2:
        raise AssertionError("refined generator no longer has exact 1/r^2 next layer")
    B2 = g2.coefficient_at_power(rem2, r, -2)
    N2 = ms(
        B2
        + B1 * P1
        - P1 * B1
        - P1 * D0 * P1
        + P1 * P1 * D0
        + P1
    )
    plus_obstruction = simp(N2[2, 3])
    minus_obstruction = simp(N2[4, 5])
    if plus_obstruction != 0 or minus_obstruction != 0:
        raise AssertionError(
            "k=1 oscillatory resonance obstruction reappeared: "
            f"plus={sp.sstr(plus_obstruction)}, minus={sp.sstr(minus_obstruction)}"
        )

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

    # Second normal form, stage A: remove every nonresonant same-exponential
    # off-diagonal N2 entry by W=(I+Q1/r)V.  Since Q1 commutes with D0, the
    # r^-2 homological coefficient is nu_i-nu_j+1.  Its only zeros are the
    # two already-certified high->low k=1 resonance directions, whose N2
    # numerators are exactly zero.
    Q1 = sp.zeros(6, 6)
    same_mu_removed = 0
    resonant_zero_count = 0
    for i in range(6):
        for j in range(6):
            if i == j or simp(mus[i] - mus[j]) != 0:
                continue
            denominator = simp(nus[i] - nus[j] + 1)
            if denominator == 0:
                if simp(N2[i, j]) != 0:
                    raise AssertionError(
                        f"second-normal-form resonance is obstructed at ({i},{j}): {sp.sstr(N2[i,j])}"
                    )
                resonant_zero_count += 1
            elif simp(N2[i, j]) != 0:
                Q1[i, j] = simp(-N2[i, j] / denominator)
                same_mu_removed += 1
    Q1 = ms(Q1)
    N2_same = ms(N2 + D1 * Q1 - Q1 * D1 + Q1)

    same_mu_residuals: list[tuple[int, int, sp.Expr]] = []
    for i in range(6):
        for j in range(6):
            if i != j and simp(mus[i] - mus[j]) == 0:
                value = simp(N2_same[i, j])
                if value != 0:
                    same_mu_residuals.append((i, j, value))
    if same_mu_residuals:
        raise AssertionError(f"same-mu N2 off-diagonal terms remain: {same_mu_residuals}")

    T_same = sp.eye(6) + s * Q1
    if simp(T_same.det().subs(s, 0) - 1) != 0:
        raise AssertionError("same-mu second-order gauge is not invertible at infinity")

    # Second normal form, stage B: remove every remaining cross-exponential
    # N2 entry by a P2/r^2 gauge.  At this order the homological denominator
    # is simply mu_i-mu_j, nonzero by construction for all such entries.
    P2 = sp.zeros(6, 6)
    cross_mu_removed_second = 0
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            gap = simp(mus[i] - mus[j])
            if gap != 0 and simp(N2_same[i, j]) != 0:
                P2[i, j] = simp(-N2_same[i, j] / gap)
                cross_mu_removed_second += 1
    P2 = ms(P2)
    N2_final = ms(N2_same + D0 * P2 - P2 * D0)
    remaining_second_offdiag = off_diagonal_nonzero(N2_final)
    if remaining_second_offdiag:
        raise AssertionError(
            f"second normal form is not diagonal: {remaining_second_offdiag}"
        )

    D2_values = [simp(N2_final[i, i]) for i in range(6)]
    D2 = sp.diag(*D2_values)
    if any(value != 0 for value in ms(N2_final - D2)):
        raise AssertionError("second normal-form diagonal extraction failed")

    T_cross2 = sp.eye(6) + s**2 * P2
    if simp(T_cross2.det().subs(s, 0) - 1) != 0:
        raise AssertionError("cross-mu second-order gauge is not invertible at infinity")

    # G is analytic in s at zero, S is constant, and all three gauges are
    # analytic and invertible at s=0.  The exact coefficient cancellations
    # above therefore imply that the fully transformed analytic generator has
    # Taylor coefficients D0,D1,D2 through s^2 and an O(s^3)=O(r^-3) remainder.

    # Once the two k=1 equations are compatible, every later projected
    # denominator is nonzero because there are no further positive-integer
    # differences in the same exponential block. The complement component
    # is solved uniquely at every order by (mu I-G_inf) on the direct sum of
    # all other eigenspaces. This closes the formal induction.

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_FORMAL_BASIS_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("INFINITY_VARIABLE := s=1/r")
    print(f"EXACT_GENERATOR_NONZERO_ANALYTIC_ENTRIES := {analytic_entries}")
    print("GENERATOR_ANALYTIC_AT_INFINITY := every exact rational entry is analytic at s=0")
    print("REFINED_CONSTANT_BASIS := exact dual basis diagonalizing G_inf and the same-mu G_1 restrictions")
    print(f"EXPONENTIAL_RATES := {[sp.sstr(x) for x in mus]}")
    print(f"POWER_EXPONENTS := {[sp.sstr(x) for x in nus]}")
    print(f"CROSS_EXPONENTIAL_HOMOLOGICAL_DENOMINATORS_USED := {cross_gap_count}")
    print("FIRST_NORMAL_FORM_LAYER := D1=diag(power exponents)/r")
    print("FIRST_NEAR_IDENTITY_GAUGE := I+s*P1 with det at s=0 equal to 1")
    print(f"POSITIVE_INTEGER_SAME_EXPONENTIAL_RESONANCES := {resonances}")
    print(f"OSCILLATORY_PLUS_K1_RESONANT_OBSTRUCTION_RECHECK := {sp.sstr(plus_obstruction)}")
    print(f"OSCILLATORY_MINUS_K1_RESONANT_OBSTRUCTION_RECHECK := {sp.sstr(minus_obstruction)}")
    print("K1_RESONANCE_COMPATIBILITY := both exact obstruction values recomputed as zero")
    print(f"SECOND_NORMAL_FORM_SAME_MU_NONRESONANT_ENTRIES_REMOVED := {same_mu_removed}")
    print(f"SECOND_NORMAL_FORM_RESONANT_ZERO_ENTRIES := {resonant_zero_count}")
    print(f"SECOND_NORMAL_FORM_CROSS_MU_ENTRIES_REMOVED := {cross_mu_removed_second}")
    print(f"SECOND_NORMAL_FORM_D2_DIAGONAL := {[sp.sstr(x) for x in D2_values]}")
    print("SECOND_NORMAL_FORM := D0 + D1/r + D2/r^2 + O(r^-3), with D0,D1,D2 diagonal")
    print("SECOND_NORMAL_FORM_REMAINDER := analytic in s=1/r and O(s^3)=O(r^-3)")
    print("HIGH_OSCILLATORY_RESONANT_NORMALIZATION := free low-channel coefficient at k=1 may be set to zero")
    print("POST_K1_PROJECTED_DENOMINATORS := nonzero for every integer k>=2 in every same-exponential block")
    print("COMPLEMENT_SOLVER := (mu*I-G_inf) is invertible on the direct sum of all other exponential eigenspaces")
    print("FORMAL_INVERSE_R_RECURRENCE := all-order solvable for each of the six channels")
    print("PURE_INVERSE_R_FORMAL_CHANNEL_COUNT := 6")
    print("FORMAL_INFINITY_BASIS := six independent exp(mu*r)*r^nu pure inverse-r formal series")
    print("BOUNDARY := formal asymptotic basis and diagonal second normal form only; no actual asymptotic-solution theorem and no physical horizon-solution channel projection claimed")


if __name__ == "__main__":
    main()
