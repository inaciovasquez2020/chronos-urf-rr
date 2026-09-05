#!/usr/bin/env python3
"""Certify the classical Levinson hypotheses for the physical infinity system.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The preceding infinity gates certify an exact refined basis with

    D0 = diag(mu_j),
    D1 = diag(nu_j),

and a near-identity first gauge which removes every cross-exponential 1/r
coupling. This verifier reconstructs that gauge directly from the exact
physical-space generator and certifies the hypotheses needed by the classical
Levinson asymptotic-integration theorem:

  1. after the first gauge the perturbation of

         Lambda(r) = D0 + D1/r

     is O(r^-2), hence belongs to L^1 on a sufficiently large positive ray;

  2. the first gauge is analytic and asymptotically invertible at infinity;

  3. Lambda satisfies Levinson's pairwise dichotomy condition. In fact the
     real part of every pairwise diagonal difference has a fixed sign for
     every r>=2, so the dichotomy constants may be chosen K=0.

The O(r^-2) conclusion is checked without forming the expensive full symbolic
inverse of the gauge. Writing

    B = D0 + B1/r + R2,     R2 = O(r^-2),
    T1 = I + P1/r,

and using the exact first-layer identity

    B1 + D0 P1 - P1 D0 = D1,

the numerator in

    T1 Z' = (B T1 - T1') Z

relative to Lambda is exactly

    R2 (I + P1/r) + (B1 P1 + P1 - P1 D1)/r^2,

which is O(r^-2). Since T1 -> I, T1^-1 is bounded on some tail and the
transformed remainder is O(r^-2) as well.

This file certifies theorem hypotheses only. It does not promote the formal
channels to an actual asymptotic fundamental matrix and does not project the
physical horizon solution onto infinity channels.
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
    s = sp.symbols("s", real=True)

    G0 = ch.coefficient_at_power(G, r, 0)
    G1 = ch.coefficient_at_power(ch.ms(G - G0), r, -1)

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
        raise AssertionError("refined infinity basis lost exact duality")

    D0 = sp.diag(*mus)
    B = ms(Sinv * G * S)
    B1 = g2.coefficient_at_power(ms(B - D0), r, -1)

    P1 = sp.zeros(6, 6)
    removed = 0
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            gap = simp(mus[i] - mus[j])
            if gap != 0:
                P1[i, j] = simp(-B1[i, j] / gap)
                removed += 1
    P1 = ms(P1)

    D1 = sp.diag(*nus)
    first_layer = ms(B1 + D0 * P1 - P1 * D0)
    if any(value != 0 for value in ms(first_layer - D1)):
        raise AssertionError("first infinity normal-form layer is no longer diagonal")

    # Exact source-bound remainder before the first gauge. The preceding
    # channel calculation already exposes this layer; recompute it here so
    # the Levinson gate is self-contained.
    R2 = ms(B - D0 - B1 / r)
    r2_power = g2.max_infinity_power(R2, r)
    if r2_power > -2:
        raise AssertionError(f"pre-gauge remainder is not O(r^-2): power={r2_power}")

    # Every nonzero R2 entry must be analytic in s=1/r at s=0. Together with
    # r2_power<=-2 this makes R2=s^2*A(s) for an analytic matrix A near zero.
    analytic_r2_entries = 0
    for value in R2:
        value = simp(value)
        if value == 0:
            continue
        at_s = simp(value.subs(r, 1 / s))
        _num, den = sp.fraction(at_s)
        if simp(den.subs(s, 0)) == 0:
            raise AssertionError(
                "pre-gauge remainder lost analyticity at infinity: " + sp.sstr(value)
            )
        analytic_r2_entries += 1

    # Exact algebraic defect identity. The constant r^-2 coefficient contains
    # no hidden r-dependence. Therefore
    #
    #   defect = R2*(I+P1/r) + C2/r^2 = O(r^-2).
    C2 = ms(B1 * P1 + P1 - P1 * D1)
    if any(r in value.free_symbols for value in C2):
        raise AssertionError("first-gauge r^-2 defect coefficient depends on r")

    # T1(s)=I+s P1 is analytic and T1(0)=I exactly. Hence det T1(0)=1 and by
    # continuity T1 is invertible with bounded inverse on some s-tail.
    T1_s = sp.eye(6) + s * P1
    if any(value != 0 for value in ms(T1_s.subs(s, 0) - sp.eye(6))):
        raise AssertionError("near-identity gauge does not tend exactly to I")
    t1_det_at_infinity = sp.Integer(1)

    transformed_remainder_power = -2

    # Exact real parts of the diagonal principal coefficients. Recheck them
    # against the symbolic channel values so the dichotomy calculation is
    # source-bound rather than a detached hard-coded table.
    re_mus = [
        sp.Rational(1, 4),
        -sp.Rational(1, 4),
        sp.Integer(0),
        sp.Integer(0),
        sp.Integer(0),
        sp.Integer(0),
    ]
    re_nus = [
        sp.Rational(3, 2),
        sp.Rational(1, 2),
        sp.Integer(0),
        sp.Integer(1),
        sp.Integer(0),
        sp.Integer(1),
    ]
    for i in range(6):
        if simp(sp.re(mus[i]) - re_mus[i]) != 0:
            raise AssertionError(f"real exponential rate changed in channel {i}")
        if simp(sp.re(nus[i]) - re_nus[i]) != 0:
            raise AssertionError(f"real power exponent changed in channel {i}")

    # For Lambda_i-Lambda_j the real derivative is A+B/r. Show it has a
    # fixed sign for every r>=2. Therefore every integral
    # int_t^x Re(Lambda_i-Lambda_j) is either >=0 or <=0, which is Levinson's
    # pairwise dichotomy condition with K=0.
    dichotomy: list[tuple[str, str, str]] = []
    ordered_pair_count = 0
    zero_real_gap_pairs = 0
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            A = simp(re_mus[i] - re_mus[j])
            Bcoef = simp(re_nus[i] - re_nus[j])
            endpoint = simp(A + Bcoef / 2)

            if A > 0:
                if Bcoef < 0 and endpoint < 0:
                    raise AssertionError(
                        f"dichotomy sign changes for {names[i]}-{names[j]}"
                    )
                sign = ">=0"
            elif A < 0:
                if Bcoef > 0 and endpoint > 0:
                    raise AssertionError(
                        f"dichotomy sign changes for {names[i]}-{names[j]}"
                    )
                sign = "<=0"
            elif Bcoef > 0:
                sign = ">=0"
            elif Bcoef < 0:
                sign = "<=0"
            else:
                sign = "=0"
                zero_real_gap_pairs += 1

            dichotomy.append((names[i], names[j], sign))
            ordered_pair_count += 1

    if ordered_pair_count != 30:
        raise AssertionError("pairwise dichotomy census is incomplete")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_LEVINSON_HYPOTHESES_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("PRINCIPAL_DIAGONAL := Lambda(r)=D0+D1/r")
    print(f"EXPONENTIAL_RATES := {[sp.sstr(x) for x in mus]}")
    print(f"POWER_EXPONENTS := {[sp.sstr(x) for x in nus]}")
    print(f"FIRST_GAUGE_CROSS_EXPONENTIAL_ENTRIES_REMOVED := {removed}")
    print(f"PRE_GAUGE_REMAINDER_MAX_INFINITY_POWER := {r2_power}")
    print(f"PRE_GAUGE_REMAINDER_ANALYTIC_NONZERO_ENTRIES := {analytic_r2_entries}")
    print("FIRST_GAUGE_DEFECT_IDENTITY := R2*(I+P1/r)+(B1*P1+P1-P1*D1)/r^2")
    print(f"FIRST_GAUGE_TRANSFORMED_REMAINDER_MAX_INFINITY_POWER := {transformed_remainder_power}")
    print(f"FIRST_GAUGE_DETERMINANT_AT_INFINITY := {t1_det_at_infinity}")
    print("FIRST_GAUGE_TAIL_INVERTIBILITY := T1(s) analytic with T1(0)=I, hence bounded inverse on some tail")
    print("L1_PERTURBATION := certified because O(r^-2) is integrable on [R,infinity)")
    print(f"LEVINSON_DICHOTOMY_ORDERED_PAIR_COUNT := {ordered_pair_count}")
    print(f"LEVINSON_ZERO_REAL_GAP_ORDERED_PAIR_COUNT := {zero_real_gap_pairs}")
    print("LEVINSON_DICHOTOMY_RAY := r>=2")
    print("LEVINSON_DICHOTOMY_CONSTANT := K=0 for every ordered channel pair")
    print(f"LEVINSON_PAIRWISE_SIGNS := {dichotomy}")
    print("LEVINSON_HYPOTHESES := exact diagonal principal part + L1 perturbation + pairwise dichotomy certified")
    print("BOUNDARY := hypotheses only; no application of the asymptotic-integration theorem, no actual infinity fundamental matrix, and no physical horizon-solution channel projection claimed")


if __name__ == "__main__":
    main()
