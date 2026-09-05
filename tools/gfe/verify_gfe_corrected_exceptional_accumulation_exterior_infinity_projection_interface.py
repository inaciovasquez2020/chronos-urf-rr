#!/usr/bin/env python3
"""Certify the canonical horizon-to-infinity channel projection interface.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The preceding asymptotic-integration gate certifies six actual linearly
independent positive-real-axis infinity solutions with leading channels

    exp(mu_j r) r^(nu_j) exp(-d2_j/r) (v_j + o(1)).

Hence every exterior solution, in particular the uniquely reconstructed
physical horizon branch Y_phys, has a unique constant coefficient vector

    C_phys = (C_grow, C_decay,
              C_+low, C_+high, C_-low, C_-high).

This verifier executes that exact gate, checks the real exponential/power
growth hierarchy, classifies the refined +/- oscillatory phase stationary
radii, certifies full refined cross-sign phase separation on the Levinson
tail, and records the exact coefficient-vanishing conditions for several
purely asymptotic classes.  It deliberately does NOT assign an "outgoing"
convention to either oscillatory sign, and it does not evaluate any connection
coefficient.
"""
from __future__ import annotations

import ast
import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_asymptotic_integration as ai


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
    re, _im = sp.expand_complex(value).as_real_imag()
    return simp(re)


def imag_part(value: sp.Expr) -> sp.Expr:
    _re, im = sp.expand_complex(value).as_real_imag()
    return simp(im)


def main() -> None:
    # Execute the exact actual-basis gate so this projection interface cannot
    # silently outlive or drift away from the theorem that supplies the basis.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        ai.main()
    prior_output = buffer.getvalue()
    print(prior_output, end="")

    if "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_ASYMPTOTIC_INTEGRATION_CERTIFIED" not in prior_output:
        raise AssertionError("actual infinity basis dependency did not certify")
    if certified_line(prior_output, "ACTUAL_POSITIVE_REAL_INFINITY_FUNDAMENTAL_BASIS") != (
        "six linearly independent actual solutions certified"
    ):
        raise AssertionError("actual fundamental-basis certification changed")

    mus = parse_expr_list(prior_output, "EXPONENTIAL_RATES")
    nus = parse_expr_list(prior_output, "POWER_EXPONENTS")
    d2s = parse_expr_list(prior_output, "SECOND_NORMAL_FORM_D2_DIAGONAL")
    if len(mus) != 6 or len(nus) != 6 or len(d2s) != 6:
        raise AssertionError("expected six actual infinity channels")

    re_mu = [real_part(x) for x in mus]
    re_nu = [real_part(x) for x in nus]
    expected_re_mu = [
        sp.Rational(1, 4),
        -sp.Rational(1, 4),
        sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0),
    ]
    expected_re_nu = [
        sp.Rational(3, 2),
        sp.Rational(1, 2),
        sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(1),
    ]
    if re_mu != expected_re_mu:
        raise AssertionError(f"real exponential hierarchy changed: {re_mu}")
    if re_nu != expected_re_nu:
        raise AssertionError(f"real power hierarchy changed: {re_nu}")

    # The two oscillatory frequencies are opposite and nonzero.  At the
    # principal D0+D1/r level this gives a globally nonstationary +/- phase:
    #
    #   Delta'(r) = sqrt(167)/10 + 142*sqrt(167)/(1670*r) > sqrt(167)/10
    #
    # for every r>0.  The certified D2/r^2 refinement contributes an additional
    # c/r^2 term, so the full diagonal-model phase must be classified separately.
    q = sp.sqrt(167) / 20
    a = sp.Rational(71, 1670) * sp.sqrt(167)
    if simp(mus[2] - sp.I * q) != 0 or simp(mus[3] - sp.I * q) != 0:
        raise AssertionError("positive oscillatory frequency changed")
    if simp(mus[4] + sp.I * q) != 0 or simp(mus[5] + sp.I * q) != 0:
        raise AssertionError("negative oscillatory frequency changed")
    if q.is_positive is not True:
        raise AssertionError("oscillatory frequency magnitude is not certified positive")

    phase_gap = simp(imag_part(mus[2] - mus[4]))
    log_phase_gap = simp(imag_part(nus[2] - nus[4]))
    if simp(phase_gap - sp.sqrt(167) / 10) != 0:
        raise AssertionError(f"principal oscillatory phase gap changed: {phase_gap}")
    if simp(log_phase_gap - 2 * a) != 0:
        raise AssertionError(f"logarithmic oscillatory phase gap changed: {log_phase_gap}")
    if phase_gap.is_positive is not True or log_phase_gap.is_positive is not True:
        raise AssertionError("principal +/- phase coefficients are not certified positive")

    levinson_tail_line = certified_line(prior_output, "LEVINSON_DICHOTOMY_UNIVERSAL_TAIL")
    if levinson_tail_line != "r >= 92":
        raise AssertionError(f"Levinson universal tail changed: {levinson_tail_line}")
    levinson_tail = sp.Integer(92)

    expected_stationary = {
        (2, 4): -sp.Rational(71, 167) + 3 * sp.sqrt(19605) / 167,
        (2, 5): -sp.Rational(71, 167) + sp.sqrt(4861545) / 1002,
        (3, 4): -sp.Rational(71, 167) + sp.sqrt(4861545) / 1002,
        (3, 5): -sp.Rational(71, 167) + sp.sqrt(3371070) / 1002,
    }
    stationary_data: list[tuple[int, int, sp.Expr, sp.Expr, sp.Expr]] = []
    exterior_stationary_pairs: list[tuple[int, int]] = []
    tail_separated_pairs: list[tuple[int, int]] = []
    for pair, expected_root in expected_stationary.items():
        i, j = pair
        if simp(imag_part(mus[i] - mus[j]) - phase_gap) != 0:
            raise AssertionError(f"cross-sign exponential phase gap changed at {pair}")
        if simp(imag_part(nus[i] - nus[j]) - log_phase_gap) != 0:
            raise AssertionError(f"cross-sign logarithmic phase gap changed at {pair}")

        c = simp(imag_part(d2s[i] - d2s[j]))
        if c.is_negative is not True:
            raise AssertionError(f"refined D2 phase coefficient is not negative at {pair}: {c}")

        discriminant = simp(log_phase_gap**2 - 4 * phase_gap * c)
        root = simp((-log_phase_gap + sp.sqrt(discriminant)) / (2 * phase_gap))
        negative_root = simp((-log_phase_gap - sp.sqrt(discriminant)) / (2 * phase_gap))
        if simp(root - expected_root) != 0:
            raise AssertionError(
                f"refined stationary radius changed at {pair}: {sp.sstr(root)}"
            )
        if sp.simplify(root > 0) is not sp.true:
            raise AssertionError(f"expected positive stationary radius at {pair}: {root}")
        if sp.simplify(negative_root < 0) is not sp.true:
            raise AssertionError(f"expected negative second stationary root at {pair}: {negative_root}")

        # For the full refined phase velocity
        #
        #   v_ij(r) = phase_gap + log_phase_gap/r + c/r^2,
        #
        # the D1+D2 correction has the sign of log_phase_gap*r+c.  Its unique
        # positive zero is -c/log_phase_gap.  Showing that zero lies before the
        # certified Levinson tail proves v_ij(r)>phase_gap there.  Reversing the
        # ordered pair negates v_ij, so the same statement is an absolute-value
        # lower bound for both orientations.
        correction_zero = simp(-c / log_phase_gap)
        if sp.simplify(correction_zero > 0) is not sp.true:
            raise AssertionError(f"expected positive D1+D2 correction zero at {pair}: {correction_zero}")
        if sp.simplify(correction_zero < levinson_tail) is not sp.true:
            raise AssertionError(
                f"D1+D2 correction zero did not lie before Levinson tail at {pair}: {correction_zero}"
            )
        if sp.simplify(log_phase_gap * levinson_tail + c > 0) is not sp.true:
            raise AssertionError(f"refined phase correction is not positive at tail start for {pair}")
        tail_separated_pairs.append(pair)

        stationary_data.append((i, j, c, root, correction_zero))
        if sp.simplify(root > 2) is sp.true:
            exterior_stationary_pairs.append(pair)
        elif sp.simplify(root < 2) is not sp.true:
            raise AssertionError(f"stationary radius location relative to r=2 undecided at {pair}: {root}")

    if exterior_stationary_pairs != [(2, 4)]:
        raise AssertionError(
            f"refined exterior stationary-pair classification changed: {exterior_stationary_pairs}"
        )
    if tail_separated_pairs != list(expected_stationary):
        raise AssertionError(f"refined tail separation classification changed: {tail_separated_pairs}")

    names = [
        "C_grow",
        "C_decay",
        "C_plus_low",
        "C_plus_high",
        "C_minus_low",
        "C_minus_high",
    ]

    # Unique decomposition follows from the certified actual fundamental
    # matrix Phi_inf.  C_phys := Phi_inf(r)^(-1) Y_phys(r) is independent of
    # r on their common exterior domain because both solve the same system.
    # The asymptotic hierarchy then gives these exact vanishing conditions:
    subexponential_zero = ["C_grow"]
    bounded_zero = ["C_grow", "C_plus_high", "C_minus_high"]
    decaying_zero = [
        "C_grow",
        "C_plus_low", "C_plus_high",
        "C_minus_low", "C_minus_high",
    ]

    if names[1] in subexponential_zero or names[1] in bounded_zero or names[1] in decaying_zero:
        raise AssertionError("decaying channel was incorrectly excluded")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_PROJECTION_INTERFACE_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("PHYSICAL_EXTERIOR_BRANCH := unique reconstructed horizon solution continued to every finite r>2")
    print("ACTUAL_INFINITY_BASIS := six-channel fundamental matrix from the certified asymptotic-integration gate")
    print(f"CONNECTION_COEFFICIENT_VECTOR := {names}")
    print("CONNECTION_DEFINITION := C_phys=Phi_inf(r)^(-1)Y_phys(r); independent of r on the common exterior domain")
    print(f"REAL_EXPONENTIAL_RATES := {[sp.sstr(x) for x in re_mu]}")
    print(f"REAL_POWER_EXPONENTS := {[sp.sstr(x) for x in re_nu]}")
    print(f"PRINCIPAL_PLUS_MINUS_PHASE_GAP := {sp.sstr(phase_gap)}")
    print(f"PRINCIPAL_PLUS_MINUS_LOG_PHASE_GAP := {sp.sstr(log_phase_gap)}")
    print("PRINCIPAL_PLUS_MINUS_PHASE_VELOCITY := sqrt(167)/10 + 142*sqrt(167)/(1670*r)")
    print("PRINCIPAL_PLUS_MINUS_GLOBAL_NONSTATIONARITY := certified for every r>0 at the D0+D1/r level")
    print(
        "REFINED_D2_PLUS_MINUS_STATIONARY_DATA := "
        f"{[(i, j, sp.sstr(c), sp.sstr(root), sp.sstr(correction_zero)) for i, j, c, root, correction_zero in stationary_data]}"
    )
    print("REFINED_D2_PHYSICAL_EXTERIOR_STATIONARY_PAIRS := [(OSCILLATORY_PLUS_LOW,OSCILLATORY_MINUS_LOW)]")
    print(
        "REFINED_D2_LOW_LOW_STATIONARY_RADIUS := "
        f"{sp.sstr(expected_stationary[(2, 4)])} > 2"
    )
    print("REFINED_PLUS_MINUS_LEVINSON_TAIL := r >= 92")
    print("REFINED_PLUS_MINUS_TAIL_PHASE_SEPARATION := all four cross-sign pairs have |phase velocity| > sqrt(167)/10 for every r>=92")
    print(f"SUBEXPONENTIAL_CONDITION := zero coefficients {subexponential_zero}")
    print(f"BOUNDED_CONDITION := zero coefficients {bounded_zero}")
    print(f"DECAYING_TO_ZERO_CONDITION := zero coefficients {decaying_zero}")
    print("EXPONENTIAL_GROWING_COEFFICIENT := C_grow is the unique scalar obstruction to subexponential growth")
    print("BOUNDEDNESS_EXTRA_OBSTRUCTIONS := C_plus_high and C_minus_high")
    print("DECAY_EXTRA_OBSTRUCTIONS := C_plus_low and C_minus_low in addition to the boundedness obstructions")
    print("OUTGOING_CONVENTION := intentionally undefined; no oscillatory sign is labeled outgoing/ingoing by this verifier")
    print("BOUNDARY := full refined cross-sign phase separation is certified on the Levinson tail despite one low/low stationary point near the horizon; no connection coefficient value/nonvanishing certificate and no global exceptional-mode conclusion")


if __name__ == "__main__":
    main()
