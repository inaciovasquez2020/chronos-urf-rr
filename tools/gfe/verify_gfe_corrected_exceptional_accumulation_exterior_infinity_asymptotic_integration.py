#!/usr/bin/env python3
"""Certify positive-real infinity asymptotic integration for the flagship sector.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The preceding formal-infinity verifier derives, from the exact physical-space
six-state generator, an analytic near-identity normal form

    Z' = (D0 + D1/r + D2/r^2 + R(r)) Z,

where D0,D1,D2 are diagonal and R(r)=O(r^-3) as r->+infinity.
This verifier executes that exact gate, parses its certified diagonal data,
and checks the two remaining hypotheses of the classical Levinson theorem:

  * R is L^1 on a sufficiently far positive-real tail;
  * every ordered pair of diagonal phases satisfies Levinson dichotomy.

The pairwise real phase derivative is

    a_ij + b_ij/r + c_ij/r^2,

with exact rational a_ij,b_ij,c_ij.  A universal tail r>=92 makes the sign
controlled by the first nonzero member of (a_ij,b_ij,c_ij).  Hence every
ordered pair obeys one of the two Levinson integral inequalities.

The standard Levinson asymptotic-integration theorem therefore yields six
actual linearly independent positive-real-axis solutions asymptotic to the
six diagonal model channels.  No projection of the physical horizon branch
onto those channels, and no outgoing/decaying/quasinormal conclusion, is
claimed here.
"""
from __future__ import annotations

import ast
import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_formal_basis as fb


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def certified_line(output: str, prefix: str) -> str:
    marker = prefix + " := "
    for line in output.splitlines():
        if line.startswith(marker):
            return line[len(marker):]
    raise AssertionError(f"missing certified output line: {prefix}")


def parse_expr_list(output: str, prefix: str) -> list[sp.Expr]:
    raw = certified_line(output, prefix)
    values = ast.literal_eval(raw)
    if not isinstance(values, list):
        raise AssertionError(f"{prefix} is not a list")
    local_dict = {"I": sp.I, "sqrt": sp.sqrt}
    return [simp(sp.sympify(value, locals=local_dict)) for value in values]


def real_part(value: sp.Expr) -> sp.Expr:
    real, _imag = sp.expand_complex(value).as_real_imag()
    return simp(real)


def strict_integer_tail(bound: sp.Expr) -> int:
    bound = simp(bound)
    if bound.is_real is not True or bound.is_nonnegative is not True:
        raise AssertionError(f"tail bound is not certified nonnegative real: {bound}")
    return int(sp.floor(bound)) + 1


def main() -> None:
    # Execute the exact source-derived formal/second-normal-form gate once and
    # retain its assertions as dependencies of this stronger theorem gate.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        fb.main()
    prior_output = buffer.getvalue()
    print(prior_output, end="")

    if "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_FORMAL_BASIS_CERTIFIED" not in prior_output:
        raise AssertionError("formal infinity dependency did not certify")
    if certified_line(prior_output, "SECOND_NORMAL_FORM_REMAINDER") != (
        "analytic in s=1/r and O(s^3)=O(r^-3)"
    ):
        raise AssertionError("second-normal-form remainder certification changed")

    mus = parse_expr_list(prior_output, "EXPONENTIAL_RATES")
    nus = parse_expr_list(prior_output, "POWER_EXPONENTS")
    d2s = parse_expr_list(prior_output, "SECOND_NORMAL_FORM_D2_DIAGONAL")
    if not (len(mus) == len(nus) == len(d2s) == 6):
        raise AssertionError("expected six diagonal infinity channels")

    # The analytic O(r^-3) remainder is L^1 on some positive-real tail:
    # analyticity gives R(r)=r^-3 H(1/r) with H bounded near zero, and
    # integral_R^infinity r^-3 dr is finite.  This is the exact decay margin
    # needed by the classical Levinson theorem.
    l1_power = 3
    if l1_power <= 1:
        raise AssertionError("remainder decay is not integrable")

    counts = {"linear": 0, "log": 0, "bounded": 0}
    pair_data: list[tuple[int, int, str, sp.Expr, sp.Expr, sp.Expr, int]] = []
    universal_tail = 1

    for i in range(6):
        for j in range(6):
            if i == j:
                continue

            a = real_part(mus[i] - mus[j])
            b = real_part(nus[i] - nus[j])
            c = real_part(d2s[i] - d2s[j])
            if not (a.is_Rational is True and b.is_Rational is True and c.is_Rational is True):
                raise AssertionError(
                    f"non-rational real phase coefficients at ({i},{j}): a={a}, b={b}, c={c}"
                )

            if a != 0:
                # For r>=R, |b|/r+|c|/r^2 <= (|b|+|c|)/R.
                # Taking R > 2(|b|+|c|)/|a| forces the sign of the full
                # phase derivative to equal sign(a).
                threshold = simp(2 * (abs(b) + abs(c)) / abs(a))
                pair_tail = strict_integer_tail(threshold)
                kind = "linear"
            elif b != 0:
                # For r>=R, |c|/r^2 <= (|c|/R)/r.  Taking
                # R > 2|c|/|b| forces the sign to equal sign(b).
                threshold = simp(2 * abs(c) / abs(b))
                pair_tail = strict_integer_tail(threshold)
                kind = "log"
            else:
                # The real phase derivative is c/r^2 (or zero), so its
                # integral over every ordered interval has one fixed sign and
                # is uniformly bounded in magnitude on every far tail.
                pair_tail = 1
                kind = "bounded"

            counts[kind] += 1
            universal_tail = max(universal_tail, pair_tail)
            pair_data.append((i, j, kind, a, b, c, pair_tail))

    expected_counts = {"linear": 18, "log": 8, "bounded": 4}
    if counts != expected_counts:
        raise AssertionError(f"Levinson pair classification changed: {counts}")
    if universal_tail != 92:
        raise AssertionError(f"certified universal dichotomy tail changed: {universal_tail}")

    # Recheck the strict domination inequalities at the universal tail.  They
    # then remain valid for every larger r by the elementary bounds used above.
    R = sp.Integer(universal_tail)
    for i, j, kind, a, b, c, _pair_tail in pair_data:
        if kind == "linear":
            error_bound = simp((abs(b) + abs(c)) / R)
            if sp.simplify(error_bound < abs(a) / 2) is not sp.true:
                raise AssertionError(
                    f"linear dichotomy domination failed at ({i},{j}): {error_bound} !< {abs(a)/2}"
                )
        elif kind == "log":
            error_coefficient = simp(abs(c) / R)
            if sp.simplify(error_coefficient < abs(b) / 2) is not sp.true:
                raise AssertionError(
                    f"log dichotomy domination failed at ({i},{j}): {error_coefficient} !< {abs(b)/2}"
                )

    phases = [
        f"exp(({sp.sstr(mu)})*r)*r^({sp.sstr(nu)})*exp(-({sp.sstr(d2)})/r)"
        for mu, nu, d2 in zip(mus, nus, d2s)
    ]

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_ASYMPTOTIC_INTEGRATION_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("NORMAL_FORM := Z'=(D0+D1/r+D2/r^2+R(r))*Z with D0,D1,D2 diagonal")
    print("REMAINDER_FACTOR := R(r)=r^-3*H(1/r), H analytic and bounded on a sufficiently far tail")
    print("LEVINSON_L1_REMAINDER := integral ||R(r)|| dr < infinity on a sufficiently far positive-real tail")
    print(f"LEVINSON_DICHOTOMY_UNIVERSAL_TAIL := r >= {universal_tail}")
    print(
        "LEVINSON_DICHOTOMY_ORDERED_PAIR_COUNTS := "
        f"linear={counts['linear']}; log={counts['log']}; bounded={counts['bounded']}"
    )
    print("LEVINSON_PAIR_REAL_PHASE_DERIVATIVE := a_ij+b_ij/r+c_ij/r^2 with exact rational coefficients")
    print("LEVINSON_DICHOTOMY := certified for all 30 ordered channel pairs")
    print(f"DIAGONAL_MODEL_CHANNELS := {phases}")
    print("STANDARD_LEVINSON_THEOREM := diagonal locally continuous Lambda + L1 remainder + pairwise dichotomy gives a fundamental matrix asymptotic to the diagonal model")
    print("ACTUAL_POSITIVE_REAL_INFINITY_FUNDAMENTAL_BASIS := six linearly independent actual solutions certified")
    print("ACTUAL_CHANNEL_LEADING_ASYMPTOTICS := exp(mu*r)*r^nu*exp(-d2/r)*(refined seed + o(1))")
    print("FORMAL_TO_ACTUAL_STATUS := actual leading channel basis certified; the separately certified all-order inverse-r formal expansions are not promoted here to all-order actual remainders")
    print("BOUNDARY := no horizon-solution channel coefficients evaluated; no outgoing, decaying, finite-energy, quasinormal, or global exceptional-mode conclusion claimed")


if __name__ == "__main__":
    main()
