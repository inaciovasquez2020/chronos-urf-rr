#!/usr/bin/env python3
"""Certify the canonical horizon-to-infinity channel projection interface.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

In addition to the qualitative projection interface, this verifier constructs
an explicit quantitative O(r^-3) bound for the exact second-normal-form
remainder on a concrete positive-real tail.  The bound is deliberately
conservative and uses only exact rational/algebraic inequalities.
"""
from __future__ import annotations

import ast
import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_asymptotic_integration as ai
import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_channels as ch
import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_g2_resonance as g2


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


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


def algebraic_abs_upper(value: sp.Expr) -> sp.Rational:
    """Exact rational upper bound for |value| in Q(sqrt(167), i)."""
    q = sp.sqrt(167)
    value = sp.radsimp(simp(value))
    re, im = sp.expand_complex(value).as_real_imag()

    def part_upper(part: sp.Expr) -> sp.Rational:
        part = sp.radsimp(sp.expand(part))
        a = simp(part.subs(q, 0))
        b = simp((part - a) / q)
        if a.is_Rational is not True or b.is_Rational is not True:
            raise AssertionError(f"coefficient left Q(sqrt(167)): {sp.sstr(part)}")
        return sp.Rational(abs(a) + 13 * abs(b))

    return sp.Rational(part_upper(re) + part_upper(im))


def constant_matrix_inf_norm_upper(matrix: sp.Matrix) -> sp.Rational:
    rows = [sum((algebraic_abs_upper(matrix[i, j]) for j in range(matrix.cols)), sp.Rational(0))
            for i in range(matrix.rows)]
    return sp.Rational(max(rows))


def polynomial_matrix_inf_norm_upper(
    matrix: sp.Matrix,
    s: sp.Symbol,
    s0: sp.Rational,
) -> sp.Rational:
    row_bounds: list[sp.Rational] = []
    for i in range(matrix.rows):
        row = sp.Rational(0)
        for j in range(matrix.cols):
            entry = sp.expand(matrix[i, j])
            if entry == 0:
                continue
            poly = sp.Poly(entry, s, domain="EX")
            bound = sp.Rational(0)
            for k in range(int(poly.degree()) + 1):
                coeff = poly.coeff_monomial(s**k)
                if coeff != 0:
                    bound += algebraic_abs_upper(coeff) * s0**k
            row += bound
        row_bounds.append(sp.Rational(row))
    return sp.Rational(max(row_bounds))


def rational_entry_tail_bound(
    entry: sp.Expr,
    r: sp.Symbol,
    s: sp.Symbol,
    s0: sp.Rational,
) -> sp.Rational:
    entry = simp(entry)
    if entry == 0:
        return sp.Rational(0)
    h = sp.cancel(sp.together(entry.subs(r, 1 / s) / s**3))
    num, den = sp.fraction(h)
    try:
        pn = sp.Poly(num, s, domain=sp.QQ)
        pd = sp.Poly(den, s, domain=sp.QQ)
    except Exception as exc:
        raise AssertionError(f"physical generator tail ceased to be rational in s: {exc}") from exc

    num_upper = sp.Rational(0)
    for k in range(int(pn.degree()) + 1):
        num_upper += abs(pn.coeff_monomial(s**k)) * s0**k

    q0 = pd.coeff_monomial(1)
    if q0 == 0:
        raise AssertionError("tail denominator vanished at s=0")
    den_deviation = sp.Rational(0)
    for k in range(1, int(pd.degree()) + 1):
        den_deviation += abs(pd.coeff_monomial(s**k)) * s0**k
    den_lower = abs(q0) - den_deviation
    if not (den_lower > 0):
        raise AssertionError(
            f"coefficient-majorant denominator bound failed on s<={s0}: {sp.sstr(den_lower)}"
        )
    return sp.Rational(sp.cancel(num_upper / den_lower))


def quantitative_normal_form_tail_bound() -> tuple[int, sp.Rational, sp.Rational, sp.Rational]:
    r, G = ch.reconstruct_generator()
    G0 = ch.coefficient_at_power(G, r, 0)
    G1 = ch.coefficient_at_power(ms(G - G0), r, -1)
    G2 = ch.coefficient_at_power(ms(G - G0 - G1 / r), r, -2)
    Grem = ms(G - G0 - G1 / r - G2 / r**2)

    R0 = 4096
    s0 = sp.Rational(1, R0)
    s = sp.symbols("s", nonnegative=True)

    physical_rows: list[sp.Rational] = []
    for i in range(6):
        row = sp.Rational(0)
        for j in range(6):
            row += rational_entry_tail_bound(Grem[i, j], r, s, s0)
        physical_rows.append(sp.Rational(row))
    C_G = sp.Rational(max(physical_rows))

    q = sp.sqrt(167)
    a = simp(sp.Rational(71, 1670) * q)
    block_data = [
        (sp.Rational(1, 4), [sp.Rational(3, 2)]),
        (-sp.Rational(1, 4), [sp.Rational(1, 2)]),
        (sp.I * q / 20, [sp.I * a, 1 + sp.I * a]),
        (-sp.I * q / 20, [-sp.I * a, 1 - sp.I * a]),
    ]
    right_blocks: list[sp.Matrix] = []
    left_blocks: list[sp.Matrix] = []
    mus: list[sp.Expr] = []
    nus: list[sp.Expr] = []
    for mu, powers in block_data:
        R, L = g2.refined_block(G0, G1, mu, powers)
        right_blocks.append(R)
        left_blocks.append(L)
        mus.extend([mu] * len(powers))
        nus.extend(powers)

    S = sp.Matrix.hstack(*right_blocks)
    Sinv = sp.Matrix.vstack(*left_blocks)
    if any(value != 0 for value in ms(Sinv * S - sp.eye(6))):
        raise AssertionError("quantitative refined basis lost exact duality")

    S_norm = constant_matrix_inf_norm_upper(S)
    Sinv_norm = constant_matrix_inf_norm_upper(Sinv)
    C_B = sp.cancel(Sinv_norm * C_G * S_norm)

    D0 = sp.diag(*mus)
    D1 = sp.diag(*nus)
    B1 = ms(Sinv * G1 * S)
    B2 = ms(Sinv * G2 * S)

    P1 = sp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            gap = simp(mus[i] - mus[j])
            if gap != 0:
                P1[i, j] = simp(-B1[i, j] / gap)
    P1 = ms(P1)
    if any(value != 0 for value in ms(B1 + D0 * P1 - P1 * D0 - D1)):
        raise AssertionError("quantitative first normal-form cancellation failed")

    N2 = ms(
        B2
        + B1 * P1
        - P1 * B1
        - P1 * D0 * P1
        + P1 * P1 * D0
        + P1
    )
    Q1 = sp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            if i == j or simp(mus[i] - mus[j]) != 0:
                continue
            denominator = simp(nus[i] - nus[j] + 1)
            if denominator == 0:
                if simp(N2[i, j]) != 0:
                    raise AssertionError("quantitative same-mu resonance reappeared")
            elif simp(N2[i, j]) != 0:
                Q1[i, j] = simp(-N2[i, j] / denominator)
    Q1 = ms(Q1)
    N2_same = ms(N2 + D1 * Q1 - Q1 * D1 + Q1)

    P2 = sp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            gap = simp(mus[i] - mus[j])
            if gap != 0 and simp(N2_same[i, j]) != 0:
                P2[i, j] = simp(-N2_same[i, j] / gap)
    P2 = ms(P2)
    N2_final = ms(N2_same + D0 * P2 - P2 * D0)
    D2 = sp.diag(*[simp(N2_final[i, i]) for i in range(6)])
    if any(value != 0 for value in ms(N2_final - D2)):
        raise AssertionError("quantitative second normal form is not diagonal")

    T = ms((sp.eye(6) + s * P1) * (sp.eye(6) + s * Q1) * (sp.eye(6) + s**2 * P2))
    Bpoly = ms(D0 + s * B1 + s**2 * B2)
    Dmodel = ms(D0 + s * D1 + s**2 * D2)

    poly_residual = ms(Bpoly * T + s**2 * T.diff(s) - T * Dmodel)
    for value in poly_residual:
        poly = sp.Poly(sp.expand(value), s, domain="EX")
        for k in range(3):
            if simp(poly.coeff_monomial(s**k)) != 0:
                raise AssertionError(f"normal-form residual has unexpected s^{k} coefficient")

    polynomial_tail = ms(poly_residual / s**3)
    C_P = polynomial_matrix_inf_norm_upper(polynomial_tail, s, s0)
    eta = polynomial_matrix_inf_norm_upper(ms(T - sp.eye(6)), s, s0)
    if not (eta < 1):
        raise AssertionError(f"normal-form gauge Neumann margin failed: eta={eta}")

    C_nf = sp.cancel((C_B * (1 + eta) + C_P) / (1 - eta))
    if C_nf <= 0:
        raise AssertionError("quantitative normal-form remainder constant is not positive")
    return R0, sp.Rational(C_G), sp.Rational(eta), sp.Rational(C_nf)


def main() -> None:
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
    expected_re_mu = [sp.Rational(1, 4), -sp.Rational(1, 4), 0, 0, 0, 0]
    expected_re_nu = [sp.Rational(3, 2), sp.Rational(1, 2), 0, 1, 0, 1]
    if re_mu != expected_re_mu:
        raise AssertionError(f"real exponential hierarchy changed: {re_mu}")
    if re_nu != expected_re_nu:
        raise AssertionError(f"real power hierarchy changed: {re_nu}")

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
            raise AssertionError(f"refined stationary radius changed at {pair}: {sp.sstr(root)}")
        if sp.simplify(root > 0) is not sp.true or sp.simplify(negative_root < 0) is not sp.true:
            raise AssertionError(f"refined stationary-root signs changed at {pair}")
        correction_zero = simp(-c / log_phase_gap)
        if sp.simplify(correction_zero > 0) is not sp.true:
            raise AssertionError(f"expected positive D1+D2 correction zero at {pair}")
        if sp.simplify(correction_zero < levinson_tail) is not sp.true:
            raise AssertionError(f"D1+D2 correction zero did not lie before Levinson tail at {pair}")
        if sp.simplify(log_phase_gap * levinson_tail + c > 0) is not sp.true:
            raise AssertionError(f"refined phase correction is not positive at tail start for {pair}")
        tail_separated_pairs.append(pair)
        stationary_data.append((i, j, c, root, correction_zero))
        if sp.simplify(root > 2) is sp.true:
            exterior_stationary_pairs.append(pair)
        elif sp.simplify(root < 2) is not sp.true:
            raise AssertionError(f"stationary radius location relative to r=2 undecided at {pair}")

    if exterior_stationary_pairs != [(2, 4)]:
        raise AssertionError(f"refined exterior stationary-pair classification changed: {exterior_stationary_pairs}")
    if tail_separated_pairs != list(expected_stationary):
        raise AssertionError(f"refined tail separation classification changed: {tail_separated_pairs}")

    R0, C_G, eta, C_nf = quantitative_normal_form_tail_bound()

    names = ["C_grow", "C_decay", "C_plus_low", "C_plus_high", "C_minus_low", "C_minus_high"]
    subexponential_zero = ["C_grow"]
    bounded_zero = ["C_grow", "C_plus_high", "C_minus_high"]
    decaying_zero = ["C_grow", "C_plus_low", "C_plus_high", "C_minus_low", "C_minus_high"]
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
    print("REFINED_D2_PLUS_MINUS_STATIONARY_DATA := " + str([(i, j, sp.sstr(c), sp.sstr(root), sp.sstr(zero)) for i, j, c, root, zero in stationary_data]))
    print("REFINED_D2_PHYSICAL_EXTERIOR_STATIONARY_PAIRS := [(OSCILLATORY_PLUS_LOW,OSCILLATORY_MINUS_LOW)]")
    print(f"REFINED_D2_LOW_LOW_STATIONARY_RADIUS := {sp.sstr(expected_stationary[(2, 4)])} > 2")
    print("REFINED_PLUS_MINUS_LEVINSON_TAIL := r >= 92")
    print("REFINED_PLUS_MINUS_TAIL_PHASE_SEPARATION := all four cross-sign pairs have |phase velocity| > sqrt(167)/10 for every r>=92")
    print(f"QUANTITATIVE_NORMAL_FORM_TAIL_START := r >= {R0}")
    print(f"QUANTITATIVE_PHYSICAL_GENERATOR_R3_CONSTANT := {sp.sstr(C_G)}")
    print(f"QUANTITATIVE_NORMAL_FORM_GAUGE_ETA := {sp.sstr(eta)} < 1")
    print(f"QUANTITATIVE_NORMAL_FORM_R3_CONSTANT := {sp.sstr(C_nf)}")
    print(f"QUANTITATIVE_NORMAL_FORM_REMAINDER := ||R_nf(r)||_inf <= ({sp.sstr(C_nf)})/r^3 for every r>={R0}")
    print(f"SUBEXPONENTIAL_CONDITION := zero coefficients {subexponential_zero}")
    print(f"BOUNDED_CONDITION := zero coefficients {bounded_zero}")
    print(f"DECAYING_TO_ZERO_CONDITION := zero coefficients {decaying_zero}")
    print("EXPONENTIAL_GROWING_COEFFICIENT := C_grow is the unique scalar obstruction to subexponential growth")
    print("BOUNDEDNESS_EXTRA_OBSTRUCTIONS := C_plus_high and C_minus_high")
    print("DECAY_EXTRA_OBSTRUCTIONS := C_plus_low and C_minus_low in addition to the boundedness obstructions")
    print("OUTGOING_CONVENTION := intentionally undefined; no oscillatory sign is labeled outgoing/ingoing by this verifier")
    print("BOUNDARY := explicit quantitative O(r^-3) second-normal-form remainder bound is certified on a concrete tail; no finite-radius growing-dual enclosure, no connection coefficient value/nonvanishing certificate, and no global exceptional-mode conclusion")


if __name__ == "__main__":
    main()
