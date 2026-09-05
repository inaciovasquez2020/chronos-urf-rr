#!/usr/bin/env python3
"""Reduce C_grow nonvanishing to a validated finite-radius state test.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The merged infinity-projection certificate supplies an exact second normal
form

    Z' = (D0 + D1/r + D2/r^2 + R_nf(r)) Z

on a concrete tail r>=4096, together with

    ||R_nf(r)||_inf <= C_nf/r^3.

The growing channel has strictly larger real exponential rate than every
other channel.  This verifier constructs the hypotheses for the normalized
growing adjoint Volterra equation, proves it is a contraction on the merged
quantitative tail, and derives a concrete finite-radius sufficient criterion
for C_grow != 0.

It does NOT numerically integrate the physical horizon solution to r=4096.
That validated finite-radius enclosure is intentionally left as the next
separate object.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_channels as ch
import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_g2_resonance as g2
import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_projection_interface as proj


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def real_part(value: sp.Expr) -> sp.Expr:
    re, _im = sp.expand_complex(value).as_real_imag()
    return simp(re)


def reconstruct_normal_form() -> tuple[
    sp.Symbol,
    sp.Matrix,
    sp.Matrix,
    list[sp.Expr],
    list[sp.Expr],
    list[sp.Expr],
]:
    """Return r, S, T(s), mu, nu, d2 for the merged exact normal form."""
    r, G = ch.reconstruct_generator()
    G0 = ch.coefficient_at_power(G, r, 0)
    G1 = ch.coefficient_at_power(ms(G - G0), r, -1)
    G2 = ch.coefficient_at_power(ms(G - G0 - G1 / r), r, -2)

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
        raise AssertionError("refined infinity basis lost exact duality")

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
        raise AssertionError("first infinity normal-form cancellation changed")

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
                    raise AssertionError("same-rate second-order resonance reappeared")
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
    d2s = [simp(N2_final[i, i]) for i in range(6)]
    D2 = sp.diag(*d2s)
    if any(value != 0 for value in ms(N2_final - D2)):
        raise AssertionError("second infinity normal form is no longer diagonal")

    s = sp.symbols("s")
    T = ms((sp.eye(6) + s * P1) * (sp.eye(6) + s * Q1) * (sp.eye(6) + s**2 * P2))
    if simp(T.det().subs(s, 0) - 1) != 0:
        raise AssertionError("combined near-identity gauge lost invertibility at infinity")

    return r, S, T, mus, nus, d2s


def main() -> None:
    r, S, T, mus, nus, d2s = reconstruct_normal_form()
    R0, _C_G, eta, C_nf = proj.quantitative_normal_form_tail_bound()
    R0 = sp.Integer(R0)
    C_nf = sp.Rational(C_nf)

    if R0 != 4096:
        raise AssertionError(f"quantitative normal-form tail changed: {R0}")
    if not (0 < eta < 1):
        raise AssertionError(f"normal-form gauge margin is not in (0,1): {eta}")
    if C_nf <= 0:
        raise AssertionError("normal-form r^-3 constant is not positive")

    # The growing diagonal channel is index 0.  Its exact scalar phase is
    # phi_0(r)=mu_0*r+nu_0*log(r)-d2_0/r.
    if mus[0] != sp.Rational(1, 4):
        raise AssertionError("growing exponential rate changed")
    if nus[0] != sp.Rational(3, 2):
        raise AssertionError("growing power exponent changed")
    if d2s[0] != sp.Rational(135, 16):
        raise AssertionError("growing D2 coefficient changed")

    # For p(r) in the normalized adjoint Psi_grow=e^{-phi_0}p, the
    # off-growing Volterra kernels contain exp(-int_r^t(lambda_0-lambda_j)).
    # Certify a uniform real gap delta=1/4 on the full quantitative tail.
    delta = sp.Rational(1, 4)
    gap_data: list[tuple[int, sp.Expr, sp.Expr, sp.Expr]] = []
    for j in range(1, 6):
        a = real_part(mus[0] - mus[j])
        b = real_part(nus[0] - nus[j])
        c = real_part(d2s[0] - d2s[j])
        if sp.simplify(a >= delta) is not sp.true:
            raise AssertionError(f"growing real exponential gap weakened at channel {j}: {a}")
        if sp.simplify(b >= 0) is not sp.true:
            raise AssertionError(f"growing real logarithmic gap is negative at channel {j}: {b}")
        if sp.simplify(c >= 0) is not sp.true:
            raise AssertionError(f"growing real D2 gap is negative at channel {j}: {c}")
        gap_data.append((j, a, b, c))

    # The merged certificate bounds the matrix infinity norm (maximum row
    # sum).  For a row vector p acting on R_nf, the maximum column sum is at
    # most 6 times that bound.  Therefore the normalized adjoint Volterra map
    # has the following exact contraction majorants on r>=R0.
    dimension = sp.Integer(6)
    q_component0 = simp(dimension * C_nf / (2 * R0**2))
    q_offdiag = simp(dimension * C_nf / (delta * R0**3))
    q = q_component0 if q_component0 >= q_offdiag else q_offdiag

    if sp.simplify(q < sp.Rational(1, 1000)) is not sp.true:
        raise AssertionError(f"adjoint Volterra contraction is not <1/1000: {q}")
    epsilon = simp(q / (1 - q))
    pairing_error = simp(dimension * epsilon)
    if sp.simplify(pairing_error < sp.Rational(1, 200)) is not sp.true:
        raise AssertionError(
            f"six-component finite-radius pairing error is not <1/200: {pairing_error}"
        )

    # Check the exact finite-radius gauge used in the criterion is invertible.
    s0 = sp.Rational(1, R0)
    T0 = ms(T.subs({next(iter(T.free_symbols)): s0})) if T.free_symbols else T
    if simp(T0.det()) == 0:
        raise AssertionError("normal-form gauge is singular at the certified tail radius")
    if simp(S.det()) == 0:
        raise AssertionError("refined constant infinity basis is singular")

    # Banach's fixed-point theorem applied to the normalized adjoint Volterra
    # operator now gives a unique p with p(infinity)=e_0^T and
    # ||p-e_0^T||_inf <= epsilon.  For the physical state,
    # Z=T(1/r)^(-1)S^(-1)Y_phys, the exact connection invariant is
    # C_grow=e^{-phi_0} p Z.  Hence
    # |C_grow-e^{-phi_0}Z_0| <= 6*epsilon*e^{-phi_0}||Z||_inf.
    # The strict 1/200 margin below is therefore a sufficient nonvanishing
    # test using only a validated enclosure of Z(R0).

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_CGROW_ADJOINT_REDUCTION_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print(f"TAIL_RADIUS := {R0}")
    print("NORMAL_FORM_STATE := Z=T(1/r)^(-1)*S^(-1)*Y_phys")
    print("GROWING_MODEL_PHASE := phi_grow(r)=r/4+(3/2)*log(r)-135/(16*r)")
    print(f"GROWING_REAL_GAP_LOWER_BOUND := {sp.sstr(delta)}")
    print(f"GROWING_GAP_DATA := {[(j, sp.sstr(a), sp.sstr(b), sp.sstr(c)) for j, a, b, c in gap_data]}")
    print(f"NORMAL_FORM_R3_CONSTANT := {sp.sstr(C_nf)}")
    print(f"ADJOINT_COLUMN_FACTOR := {dimension}")
    print(f"VOLTERRA_COMPONENT0_BOUND := {sp.sstr(q_component0)}")
    print(f"VOLTERRA_OFFDIAGONAL_BOUND := {sp.sstr(q_offdiag)}")
    print(f"VOLTERRA_CONTRACTION_FACTOR := {sp.sstr(q)} < 1/1000")
    print(f"VOLTERRA_FIXED_POINT_ERROR := epsilon={sp.sstr(epsilon)}")
    print(f"SIX_COMPONENT_PAIRING_ERROR := 6*epsilon={sp.sstr(pairing_error)} < 1/200")
    print("CGROW_ADJOINT := unique normalized physical adjoint row Psi_grow=e^(-phi_grow)*p with p(infinity)=e_0^T")
    print("CGROW_INVARIANT := C_grow=Psi_grow(r)*Y_phys(r)=e^(-phi_grow(r))*p(r)*Z(r)")
    print("MODEL_FINITE_RADIUS_COORDINATE := Chat=e^(-phi_grow(R0))*Z_0(R0)")
    print("FINITE_RADIUS_ERROR := |C_grow-Chat| <= 6*epsilon*e^(-phi_grow(R0))*||Z(R0)||_inf")
    print("CERTIFIED_NONVANISHING_TEST := |Z_0(R0)| > ||Z(R0)||_inf/200 => C_grow != 0")
    print("BOUNDARY := finite-radius transformed physical state Z(4096) is not yet interval-enclosed; C_grow value/nonvanishing and global exceptional-mode conclusion remain unproved")


if __name__ == "__main__":
    main()
