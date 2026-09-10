#!/usr/bin/env python3
"""Certify the first constraint-adapted cascade of the scaled horizon system.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The certified power-scaled logarithmic exterior system is

    U_t = (R/x + H_reg(x)) U,       x=r-2,

with rank-one nilpotent residue

    R = -(5/18) e_5 (e_0^T + e_4^T).

The raw scaled generator is therefore not horizon-regular.  Instead of hiding
that irregular term, this verifier exposes the exact constraint combination
that carries it and the first derivative companion:

    C0 = U0 + U4,
    C1 = -2 U0 + U1 + U5.

It proves exactly

    C0_t = (3/2) C0 + C1,
    C1_t = -(5/18) C0/x + L1(x) U,

where L1(x) is rational and horizon-regular.  The already-certified physical
log-plus-ordinary generalized-Frobenius data imply

    C0/x ->  3/5,
    C1/x -> -3/10.

The resulting leading cancellation in C1_t is checked exactly.  This is the
first constraint-adapted blow-up layer for a later validated propagator; it is
not a claim that the full six-state irregular singularity has been removed.
"""
from __future__ import annotations

import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_double_laplace as dl
import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_prefix as prefix
import verify_gfe_corrected_exceptional_accumulation_borel_top_log_local_majorant as local
import verify_gfe_corrected_exceptional_accumulation_exterior_horizon_scaled_log_system as scaled


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def build_scaled_system() -> tuple[sp.Symbol, sp.Matrix, sp.Matrix, sp.Matrix]:
    r, G = scaled.build_generator()
    x = sp.symbols("x", positive=True)
    powers = [
        sp.Rational(1, 2),
        sp.Rational(-1, 2),
        sp.Rational(-3, 2),
        sp.Rational(-1, 2),
        sp.Rational(-3, 2),
        sp.Rational(-5, 2),
    ]

    H = sp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            if G[i, j] == 0:
                continue
            exponent = simp(1 - powers[i] + powers[j])
            if not bool(exponent.is_integer):
                raise AssertionError(f"noninteger scaled exponent at {(i, j)}: {exponent}")
            H[i, j] = simp(x ** int(exponent) * G[i, j].subs(r, x + 2))
    for i in range(6):
        H[i, i] = simp(H[i, i] - powers[i])
    H = ms(H)

    residue = sp.zeros(6, 6)
    residue[5, 0] = sp.Rational(-5, 18)
    residue[5, 4] = sp.Rational(-5, 18)

    # Recompute the residue rather than merely trusting the displayed values
    # of the dependency certificate.
    for i in range(6):
        for j in range(6):
            value = simp(H[i, j])
            expected = residue[i, j]
            if expected != 0:
                if simp((x * value).subs(x, 0) - expected) != 0:
                    raise AssertionError(f"scaled residue entry {(i, j)} changed")
            else:
                num, den = sp.fraction(sp.together(value))
                if value != 0 and simp(den.subs(x, 0)) == 0:
                    once = simp(x * value)
                    _, once_den = sp.fraction(sp.together(once))
                    if simp(once_den.subs(x, 0)) == 0 or simp(once.subs(x, 0)) != 0:
                        raise AssertionError(f"unexpected horizon pole at {(i, j)}")

    if residue.rank() != 1 or ms(residue * residue) != sp.zeros(6, 6):
        raise AssertionError("rank-one nilpotent horizon residue changed")

    regular = ms(H - residue / x)
    for value in regular:
        if value == 0:
            continue
        _, den = sp.fraction(sp.together(value))
        if simp(den.subs(x, 0)) == 0:
            raise AssertionError("residue-subtracted generator is not horizon-regular")
    return x, H, residue, regular


def horizon_row_limit(row: sp.Matrix, x: sp.Symbol) -> sp.Matrix:
    out = sp.zeros(1, row.cols)
    for j in range(row.cols):
        value = simp(row[0, j])
        if value == 0:
            continue
        _, den = sp.fraction(sp.together(value))
        if simp(den.subs(x, 0)) == 0:
            raise AssertionError(f"row retains horizon pole at column {j}")
        out[0, j] = simp(value.subs(x, 0))
    return ms(out)


def physical_pair_from_top_coordinates(n: int, xi: sp.Expr, kap: sp.Expr) -> sp.Matrix:
    return sp.Matrix([simp(xi + kap), simp((4 * n + 2) * kap)])


def scaled_coefficient(
    n: int,
    top_log_pair: sp.Matrix,
    ordinary_pair: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return log and log-free coefficients of the six scaled U components."""
    q = sp.symbols("q")
    operators = [
        (0, sp.Integer(1)),
        (0, q + sp.Rational(1, 2)),
        (0, (q - sp.Rational(1, 2)) * (q + sp.Rational(1, 2))),
        (1, sp.Integer(1)),
        (1, q - sp.Rational(1, 2)),
        (1, (q - sp.Rational(3, 2)) * (q - sp.Rational(1, 2))),
    ]
    log_part = sp.zeros(6, 1)
    ordinary_part = sp.zeros(6, 1)
    for i, (pair_index, op) in enumerate(operators):
        op_n = simp(op.subs(q, n))
        dop_n = simp(sp.diff(op, q).subs(q, n))
        log_part[i] = simp(op_n * top_log_pair[pair_index])
        ordinary_part[i] = simp(
            op_n * ordinary_pair[pair_index] + dop_n * top_log_pair[pair_index]
        )
    return ms(log_part), ms(ordinary_part)


def main() -> None:
    # Lock the exact structural dependency and the actual all-order physical
    # asymptotic reconstruction used to turn n=0,1 coefficient identities into
    # limits of the reconstructed positive-x solution.
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        scaled.main()
    scaled_log = buf.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_HORIZON_SCALED_LOG_SYSTEM_CERTIFIED",
        "HORIZON_RESIDUE_RANK := 1",
        "PHYSICAL_LEADING_SEED_RESIDUE := 0",
        "REGULAR_REMAINDER_HORIZON_POLE_COUNT := 0",
    ]:
        if token not in scaled_log:
            raise AssertionError("scaled-system dependency changed: " + token)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        dl.main()
    dl_log = buf.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_DOUBLE_LAPLACE_RECONSTRUCTION_CERTIFIED",
        "ASYMPTOTIC_RECONSTRUCTION :=",
        "ACTUAL_ORIGINAL_EULER_SOLUTION :=",
    ]:
        if token not in dl_log:
            raise AssertionError("double-Laplace dependency changed: " + token)

    # Lock the canonical ordinary n=0,1 normalization used below.
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        prefix.main()
    prefix_log = buf.getvalue()
    for token in [
        "CANONICAL_ORDINARY_N0_PHYSICAL_VECTOR := [1,2]",
        "CANONICAL_ORDINARY_N1_PHYSICAL_VECTOR := [0,154/45]",
    ]:
        if token not in prefix_log:
            raise AssertionError("ordinary-prefix dependency changed: " + token)

    x, H, residue, regular = build_scaled_system()

    c0 = sp.Matrix([[1, 0, 0, 0, 1, 0]])
    c1 = sp.Matrix([[-2, 1, 0, 0, 0, 1]])

    # Exact first constraint evolution.  This identity uses only the kinematic
    # shift rows and is valid for every x>0, not merely asymptotically.
    c0_evolution = ms(c0 * H)
    expected_c0_evolution = ms(sp.Rational(3, 2) * c0 + c1)
    if c0_evolution != expected_c0_evolution:
        raise AssertionError("C0_t=(3/2)C0+C1 identity failed")

    # The only singular term in C1_t is precisely -(5/18) C0/x.
    c1_regular_row = ms(c1 * regular)
    c1_evolution_residual = ms(c1 * H - sp.Rational(-5, 18) * c0 / x - c1_regular_row)
    if c1_evolution_residual != sp.zeros(1, 6):
        raise AssertionError("C1 singular forcing did not factor through C0")
    c1_regular_h0 = horizon_row_limit(c1_regular_row, x)
    expected_c1_regular_h0 = sp.Matrix([[
        sp.Rational(-2299, 900),
        sp.Integer(-1),
        sp.Integer(2),
        sp.Rational(4123, 1800),
        sp.Rational(-439, 100),
        sp.Rational(-7, 2),
    ]])
    if c1_regular_h0 != expected_c1_regular_h0:
        raise AssertionError("C1 regular horizon row changed")

    # Reconstruct the n=0 and n=1 physical generalized-Frobenius scaled-state
    # coefficients.  For P(theta)[v_L x^n log x + v_O x^n], the log-free part
    # is P(n)v_O + P'(n)v_L.
    xi_l, kap_l = local.physical_prefix()
    top0 = physical_pair_from_top_coordinates(0, xi_l.get(0, 0), kap_l.get(0, 0))
    top1 = physical_pair_from_top_coordinates(1, xi_l[1], kap_l[1])
    if top0 != sp.zeros(2, 1):
        raise AssertionError("physical top-log constant term changed")
    if top1 != sp.Matrix([sp.Rational(5, 9), sp.Rational(-10, 9)]):
        raise AssertionError("physical top-log n=1 vector changed")

    ordinary0 = sp.Matrix([1, 2])
    ordinary1 = sp.Matrix([0, sp.Rational(154, 45)])
    log0, const0 = scaled_coefficient(0, top0, ordinary0)
    log1, const1 = scaled_coefficient(1, top1, ordinary1)
    physical_seed = sp.Matrix([
        1,
        sp.Rational(1, 2),
        sp.Rational(-1, 4),
        2,
        -1,
        sp.Rational(3, 2),
    ])
    if log0 != sp.zeros(6, 1) or const0 != physical_seed:
        raise AssertionError("scaled physical leading seed reconstruction changed")

    c0_log1 = simp((c0 * log1)[0])
    c1_log1 = simp((c1 * log1)[0])
    c0_const1 = simp((c0 * const1)[0])
    c1_const1 = simp((c1 * const1)[0])
    if c0_log1 != 0 or c1_log1 != 0:
        raise AssertionError("first blown-up constraints retain an x*log(x) leading term")
    if c0_const1 != sp.Rational(3, 5):
        raise AssertionError(f"C0/x physical limit changed: {c0_const1}")
    if c1_const1 != sp.Rational(-3, 10):
        raise AssertionError(f"C1/x physical limit changed: {c1_const1}")

    # The finite limit of C1_t requires an exact cancellation between the
    # singular residue forcing and the regular-row value on the leading seed.
    regular_seed_value = simp((c1_regular_h0 * physical_seed)[0])
    if regular_seed_value != sp.Rational(1, 6):
        raise AssertionError(f"C1 regular leading balance changed: {regular_seed_value}")
    leading_c1_balance = simp(
        sp.Rational(-5, 18) * c0_const1 + regular_seed_value
    )
    if leading_c1_balance != 0:
        raise AssertionError("C1 leading singular/regular balance failed")

    # B0=C0/x and B1=C1/x satisfy a regular first equation exactly:
    # B0_t=(1/2)B0+B1.  The next numerator in B1_t is exposed, not discarded.
    b0_limit = c0_const1
    b1_limit = c1_const1
    b0_rhs_limit = simp(sp.Rational(1, 2) * b0_limit + b1_limit)
    if b0_rhs_limit != 0:
        raise AssertionError("physical B0 derivative horizon limit should vanish")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_HORIZON_CONSTRAINT_CASCADE_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("SCALED_SYSTEM := U_t=(R/x+H_reg(x))*U")
    print("HORIZON_RESIDUE := R=-(5/18)*e5*(e0^T+e4^T)")
    print("HORIZON_RESIDUE_NILPOTENT := R^2=0")
    print("CONSTRAINT_C0 := U0+U4")
    print("CONSTRAINT_C1 := -2*U0+U1+U5")
    print("CONSTRAINT_C0_EVOLUTION := C0_t=(3/2)*C0+C1")
    print("CONSTRAINT_C1_EVOLUTION := C1_t=-(5/18)*C0/x+L1(x)*U")
    print("C1_REGULAR_ROW_HORIZON_LIMIT := " + sp.sstr(list(c1_regular_h0)))
    print("PHYSICAL_C0_XLOG_COEFFICIENT_AT_N1 := 0")
    print("PHYSICAL_C1_XLOG_COEFFICIENT_AT_N1 := 0")
    print("PHYSICAL_C0_OVER_X_LIMIT := 3/5")
    print("PHYSICAL_C1_OVER_X_LIMIT := -3/10")
    print("PHYSICAL_C1_REGULAR_ROW_SEED_VALUE := 1/6")
    print("PHYSICAL_C1_LEADING_BALANCE := -(5/18)*(3/5)+1/6=0")
    print("BLOWUP_B0 := C0/x")
    print("BLOWUP_B1 := C1/x")
    print("B0_EVOLUTION := B0_t=(1/2)*B0+B1")
    print("PHYSICAL_B0_HORIZON_LIMIT := 3/5")
    print("PHYSICAL_B1_HORIZON_LIMIT := -3/10")
    print("PHYSICAL_B0_T_HORIZON_LIMIT := 0")
    print("NEXT_COMPATIBILITY_NUMERATOR := C2=-(5/18)*B0+L1(x)*U; physical leading limit is 0")
    print("CONDITIONING_ROUTE := preserve C0,C1 correlation and continue the compatibility blow-up before interval propagation")
    print("BOUNDARY := first constraint-cascade/blow-up layer only; no full horizon regularization, no validated propagation to r=4096, no Z_phys(4096) enclosure, no C_grow value/nonvanishing, and no global exceptional-mode closure claimed")


if __name__ == "__main__":
    main()
