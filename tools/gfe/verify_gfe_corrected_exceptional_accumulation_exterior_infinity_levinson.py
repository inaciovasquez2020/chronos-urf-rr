#!/usr/bin/env python3
"""Certify the classical Levinson hypotheses for the physical infinity system.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The preceding infinity gates certify an exact refined basis with

    D0 = diag(mu_j),
    D1 = diag(nu_j),

and a near-identity first gauge which removes every cross-exponential 1/r
coupling.  This verifier reconstructs that gauge directly from the exact
physical-space generator and certifies the two hypotheses needed by the
classical Levinson asymptotic-integration theorem:

  1. after the first gauge the perturbation of

         Lambda(r) = D0 + D1/r

     is O(r^-2), hence belongs to L^1 on a sufficiently large positive ray;

  2. Lambda satisfies Levinson's pairwise dichotomy condition.  In fact the
     real part of every pairwise diagonal difference has a fixed sign for
     every r>=2, so the dichotomy constants may be chosen K=0.

This file certifies theorem hypotheses only.  It does not promote the formal
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

    # If Y = S*T1*Z with T1=I+P1/r, then
    #
    #   T1 Z' = (B*T1 - T1')Z.
    #
    # Since T1'=-P1/r^2, the numerator of the perturbation relative to
    # Lambda=D0+D1/r is the exact rational matrix below.  Avoiding an exact
    # symbolic inverse keeps this verifier narrow: det(T1)->1 proves T1^-1 is
    # bounded on some tail, so an O(r^-2) numerator gives an O(r^-2)
    # transformed perturbation.
    T1 = sp.eye(6) + P1 / r
    defect = ms(B * T1 + P1 / r**2 - T1 * (D0 + D1 / r))
    defect_power = g2.max_infinity_power(defect, r)
    if defect_power > -2:
        raise AssertionError(
            f"first-gauge defect is not L1-order at infinity: power={defect_power}"
        )

    det_tail = simp(T1.det().subs(r, 1 / s))
    det_at_zero = simp(det_tail.subs(s, 0))
    if det_at_zero != 1:
        raise AssertionError(
            f"near-identity gauge determinant does not tend to one: {sp.sstr(det_at_zero)}"
        )

    analytic_defect_entries = 0
    for value in defect:
        value = simp(value)
        if value == 0:
            continue
        at_s = simp(value.subs(r, 1 / s))
        _num, den = sp.fraction(at_s)
        if simp(den.subs(s, 0)) == 0:
            raise AssertionError(
                "first-gauge defect lost analyticity at infinity: "
                + sp.sstr(value)
            )
        analytic_defect_entries += 1

    # Exact real parts of the diagonal principal coefficients.  Recheck them
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

    # For Lambda_i-Lambda_j the real derivative is A+B/r.  Show it has a
    # fixed sign for every r>=2.  Therefore every integral
    # int_t^x Re(Lambda_i-Lambda_j) is either >=0 or <=0, which is Levinson's
    # dichotomy condition with K=0.
    dichotomy: list[tuple[str, str, str]] = []
    ordered_pair_count = 0
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
    print(f"FIRST_GAUGE_DEFECT_MAX_INFINITY_POWER := {defect_power}")
    print(f"FIRST_GAUGE_DEFECT_ANALYTIC_NONZERO_ENTRIES := {analytic_defect_entries}")
    print("FIRST_GAUGE_DETERMINANT_AT_INFINITY := 1")
    print("TRANSFORMED_REMAINDER := T1^-1*defect = O(r^-2) on a sufficiently large positive ray")
    print("L1_PERTURBATION := certified because O(r^-2) is integrable on [R,infinity)")
    print(f"LEVINSON_DICHOTOMY_ORDERED_PAIR_COUNT := {ordered_pair_count}")
    print("LEVINSON_DICHOTOMY_RAY := r>=2")
    print("LEVINSON_DICHOTOMY_CONSTANT := K=0 for every ordered channel pair")
    print(f"LEVINSON_PAIRWISE_SIGNS := {dichotomy}")
    print("LEVINSON_HYPOTHESES := exact diagonal principal part + L1 perturbation + pairwise dichotomy certified")
    print("BOUNDARY := hypotheses only; no application of the asymptotic-integration theorem, no actual infinity fundamental matrix, and no physical horizon-solution channel projection claimed")


if __name__ == "__main__":
    main()
