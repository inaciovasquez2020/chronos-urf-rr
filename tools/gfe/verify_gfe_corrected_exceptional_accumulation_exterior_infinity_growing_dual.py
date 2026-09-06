#!/usr/bin/env python3
"""Certify a finite-radius enclosure for the normalized growing dual.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The merged infinity-projection gate supplies a fully transformed normal form

    Z' = (D0 + D1/r + D2/r^2 + R_nf(r)) Z,

on r>=4096 with D0,D1,D2 diagonal and the explicit bound

    ||R_nf(r)||_inf <= C_nf/r^3.

The actual infinity fundamental basis also supplies the dual row selecting the
exponentially growing channel.  If

    m_g(r)=exp(mu_g*r) r^nu_g exp(-d2_g/r)

is the growing diagonal model factor and ell_g is the corresponding row of
Phi_inf(r)^(-1), define the normalized dual

    q_g(r)=m_g(r)*ell_g(r).

Then q_g(r)->e_g^T as r->infinity and

    q_g' = q_g (lambda_g I - D - R_nf).

For the growing channel, every real diagonal gap Re(lambda_g-lambda_j) is
strictly positive on r>=4096.  Hence every backward Volterra kernel has
modulus <=1.  In row l1 norm,

    ||q_g(4096)-e_g^T||_1 <= delta,
    delta = epsilon/(1-epsilon),
    epsilon = integral_4096^infinity ||R_nf(r)||_inf dr
            <= C_nf/(2*4096^2).

This yields the finite-radius scalar enclosure

    |m_g C_grow - Z_phys,0| <= delta ||Z_phys||_inf,

where Z_phys=T(r)^(-1) S^(-1) Y_phys is the certified normal-form coordinate.
Since m_g(4096)>0, the strict inequality

    |Z_phys,0| > delta ||Z_phys||_inf

is a sufficient finite-radius certificate that C_grow != 0.

This verifier constructs and checks the exact D0,D1,D2 data from the physical
six-state generator, reuses the independently source-derived quantitative
normal-form remainder constant, and certifies the enclosure radius.  It does
not yet perform validated finite-radius propagation of Y_phys to r=4096 and
therefore does not claim C_grow nonvanishing.
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


def reconstruct_diagonal_normal_form() -> tuple[
    list[sp.Expr], list[sp.Expr], list[sp.Expr]
]:
    """Reconstruct the exact diagonal D0,D1,D2 entries from the source system."""
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
    if any(value != 0 for value in ms(Sinv * G0 * S - D0)):
        raise AssertionError("refined basis no longer diagonalizes G_inf")

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

    D1 = sp.diag(*nus)
    if any(value != 0 for value in ms(B1 + D0 * P1 - P1 * D0 - D1)):
        raise AssertionError("first diagonal normal-form layer changed")

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
                    raise AssertionError(
                        f"same-mu k=1 infinity resonance reappeared at ({i},{j})"
                    )
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

    return mus, nus, d2s


def main() -> None:
    # Recompute the already-merged quantitative normal-form remainder bound.
    # This function is exact and source-derived; it also certifies the full
    # near-identity physical-to-normal gauge has a Neumann margin < 1.
    R0, _C_G, eta, C_nf = proj.quantitative_normal_form_tail_bound()
    if R0 != 4096:
        raise AssertionError(f"quantitative normal-form tail start changed: {R0}")
    if not (sp.Rational(0) <= eta < 1):
        raise AssertionError(f"normal-form gauge lost its Neumann margin: {eta}")
    if not (C_nf > 0):
        raise AssertionError("normal-form remainder constant is not positive")

    mus, nus, d2s = reconstruct_diagonal_normal_form()
    if len(mus) != 6 or len(nus) != 6 or len(d2s) != 6:
        raise AssertionError("expected six infinity channels")

    # The growing model factor is real and strictly positive for every r>0.
    if simp(mus[0] - sp.Rational(1, 4)) != 0:
        raise AssertionError("growing exponential rate changed")
    if simp(nus[0] - sp.Rational(3, 2)) != 0:
        raise AssertionError("growing power exponent changed")
    if simp(d2s[0] - sp.Rational(135, 16)) != 0:
        raise AssertionError("growing D2 exponent changed")

    # For j!=0, certify Re(lambda_g-lambda_j)>0 on the whole quantitative
    # tail.  Here lambda_j=mu_j+nu_j/r+d2_j/r^2.  Every leading real gap is
    # positive and every 1/r real gap is nonnegative.  If the 1/r^2 gap is
    # negative, its largest adverse contribution occurs at r=R0.
    gap_lower_bounds: list[sp.Expr] = []
    for j in range(1, 6):
        A = real_part(mus[0] - mus[j])
        B = real_part(nus[0] - nus[j])
        C = real_part(d2s[0] - d2s[j])
        if A.is_positive is not True:
            raise AssertionError(f"growing leading real gap is not positive against channel {j}: {A}")
        if B.is_nonnegative is not True:
            raise AssertionError(f"growing logarithmic real gap is negative against channel {j}: {B}")
        lower = simp(A + (C / R0**2 if C.is_negative is True else 0))
        if sp.simplify(lower > 0) is not sp.true:
            raise AssertionError(
                f"growing diagonal phase gap is not positive on r>={R0} against channel {j}: {lower}"
            )
        gap_lower_bounds.append(lower)

    # Row l1 is subordinate to the matrix infinity norm.  The merged bound
    # gives an exact Volterra operator norm epsilon on [R0,infinity).
    epsilon = sp.Rational(C_nf) / (2 * R0**2)
    if not (sp.Rational(0) < epsilon < 1):
        raise AssertionError(f"Volterra tail norm is not contractive: epsilon={epsilon}")
    if not (epsilon < sp.Rational(1, 1000)):
        raise AssertionError(f"expected strong tail margin epsilon<1/1000, got {epsilon}")

    delta = simp(epsilon / (1 - epsilon))
    if not (sp.Rational(0) < delta < sp.Rational(1, 1000)):
        raise AssertionError(f"normalized growing-dual radius is not small: delta={delta}")

    # The actual infinity basis already certified on main supplies the unique
    # growing dual ell_g.  Multiplication by its positive diagonal model factor
    # m_g yields q_g->e_0^T.  The backward Volterra kernels have modulus <=1
    # by the exact positive gap checks above (and equal one in the 0th slot).
    # Therefore
    #   ||q-e0||_1 <= epsilon * sup ||q||_1
    #                <= epsilon*(1+sup||q-e0||_1),
    # which gives delta=epsilon/(1-epsilon).

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_GROWING_DUAL_ENCLOSURE_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print(f"TAIL_RADIUS := {R0}")
    print("NORMAL_FORM := Z'=(D0+D1/r+D2/r^2+R_nf)Z")
    print(f"GROWING_MODEL := exp(r/4)*r^(3/2)*exp(-135/(16*r))")
    print(f"GROWING_VS_OTHER_REAL_PHASE_GAP_LOWER_BOUNDS_AT_TAIL := {[sp.sstr(x) for x in gap_lower_bounds]}")
    print("BACKWARD_GROWING_DUAL_KERNEL_MODULUS := <=1 on the entire certified tail")
    print(f"NORMAL_FORM_R3_CONSTANT := {sp.sstr(C_nf)}")
    print(f"TAIL_REMAINDER_INTEGRAL_EPSILON := {sp.sstr(epsilon)}")
    print(f"TAIL_REMAINDER_INTEGRAL_EPSILON_DECIMAL := {sp.N(epsilon, 20)}")
    print(f"NORMALIZED_GROWING_DUAL_L1_RADIUS := {sp.sstr(delta)}")
    print(f"NORMALIZED_GROWING_DUAL_L1_RADIUS_DECIMAL := {sp.N(delta, 20)}")
    print("NORMALIZED_GROWING_DUAL_CENTER := e_0^T in the certified second-normal-form coordinates")
    print("NORMALIZED_GROWING_DUAL_ENCLOSURE := ||q_g(4096)-e_0^T||_1 <= delta")
    print(f"PHYSICAL_TO_NORMAL_GAUGE_NEUMANN_ETA := {sp.sstr(eta)} < 1")
    print("FINITE_RADIUS_CONNECTION_ENCLOSURE := |m_g(4096)*C_grow-Z_phys,0(4096)| <= delta*||Z_phys(4096)||_inf")
    print("FINITE_RADIUS_CGROW_NONVANISHING_TEST := |Z_phys,0(4096)| > delta*||Z_phys(4096)||_inf implies C_grow != 0")
    print("SCALING_SIGN := m_g(4096)>0, so the scaled and unscaled growing coefficients have identical zero/nonzero status")
    print("BOUNDARY := infinity-side growing-dual enclosure only; validated forward propagation of the physical horizon solution to r=4096 and numerical/nonvanishing evaluation of C_grow remain open")


if __name__ == "__main__":
    main()
