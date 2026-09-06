#!/usr/bin/env python3
"""Certify a quantitative infinity-tail enclosure for the C_grow dual.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

The merged infinity work gives an exact second normal form

    Z' = (D0 + D1/r + D2/r^2 + R_nf(r)) Z,
    ||R_nf(r)||_inf <= C_nf/r^3

on a certified tail.  For extracting the exponentially growing coefficient it
is convenient to absorb D2/r^2 into the integrable perturbation and use the
simpler diagonal model Lambda=D0+D1/r.

For the growing channel g, write the normalized adjoint row as

    w_g(r) = exp(-phi_g(r)) q_g(r),
    phi_g'(r) = Lambda_g(r),
    q_g(infinity) = e_g^T.

Every real gap Re(Lambda_g-Lambda_j) is nonnegative (strictly positive for
j!=g).  Hence the diagonal Volterra propagators have modulus <=1.  Using the
row 1-norm together with the matrix infinity norm gives

    ||q E||_1 <= ||q||_1 ||E||_inf.

If

    M(R) = integral_R^infinity ||D2/r^2 + R_nf(r)||_inf dr < 1,

then the Volterra map is a contraction and

    ||q_g(R)-e_g^T||_1 <= M(R)/(1-M(R)).

This is the quantitative dual half of a future enclosure for C_grow.  It does
not evaluate the physical state at the same finite radius and therefore does
not yet claim C_grow != 0.
"""
from __future__ import annotations

import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_formal_basis as fb
import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_projection_interface as pi


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def real_part(value: sp.Expr) -> sp.Expr:
    re, _im = sp.expand_complex(value).as_real_imag()
    return simp(re)


def main() -> None:
    # Re-execute the exact normal-form gate so the diagonal data are not copied
    # from stale output or trusted only through CI ordering.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        fb.main()
    prior_output = buffer.getvalue()
    if "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_FORMAL_BASIS_CERTIFIED" not in prior_output:
        raise AssertionError("formal infinity dependency did not certify")

    mus = pi.parse_expr_list(prior_output, "EXPONENTIAL_RATES")
    nus = pi.parse_expr_list(prior_output, "POWER_EXPONENTS")
    d2s = pi.parse_expr_list(prior_output, "SECOND_NORMAL_FORM_D2_DIAGONAL")
    if not (len(mus) == len(nus) == len(d2s) == 6):
        raise AssertionError("expected six diagonal normal-form channels")

    if simp(mus[0] - sp.Rational(1, 4)) != 0:
        raise AssertionError("growing exponential rate changed")
    if simp(nus[0] - sp.Rational(3, 2)) != 0:
        raise AssertionError("growing power exponent changed")

    # Recompute the merged quantitative O(r^-3) bound from exact source data.
    R0, _C_G, eta, C_nf = pi.quantitative_normal_form_tail_bound()
    if R0 != 4096:
        raise AssertionError(f"quantitative normal-form tail start changed: {R0}")
    if not (eta < 1 and C_nf > 0):
        raise AssertionError("quantitative normal-form tail certificate changed")

    # Infinity-norm upper bound for the diagonal D2 matrix.  The helper uses
    # exact rational bounds in Q(sqrt(167),i), so no floating point enters.
    C2 = max(pi.algebraic_abs_upper(value) for value in d2s)
    C2 = sp.Rational(C2)
    if C2 <= 0:
        raise AssertionError("D2 norm upper bound is not positive")

    # Choose a dyadic tail far enough that the complete Volterra perturbation
    # mass is <=1/16.  Since the quantitative bound is valid from R0 onward,
    # it remains valid on every later tail.
    R = sp.Integer(R0)
    mass = simp(C2 / R + C_nf / (2 * R**2))
    for _ in range(256):
        if sp.simplify(mass <= sp.Rational(1, 16)) is sp.true:
            break
        R *= 2
        mass = simp(C2 / R + C_nf / (2 * R**2))
    else:
        raise AssertionError("could not obtain a contracting growing-dual tail")

    if sp.simplify(mass > 0) is not sp.true or sp.simplify(mass < 1) is not sp.true:
        raise AssertionError(f"Volterra perturbation mass is not in (0,1): {mass}")

    # The model gap from the growing channel to every other channel is
    # Re[(mu_g-mu_j)+(nu_g-nu_j)/r].  For these exact channels both the
    # constant and 1/r contributions are nonnegative, with a strict constant
    # gap.  Therefore every forward Volterra kernel has modulus <=1 on r>0.
    gap_data: list[tuple[int, sp.Expr, sp.Expr, sp.Expr]] = []
    for j in range(1, 6):
        a = real_part(mus[0] - mus[j])
        b = real_part(nus[0] - nus[j])
        if sp.simplify(a > 0) is not sp.true:
            raise AssertionError(f"growing-channel constant real gap is not positive for j={j}: {a}")
        if sp.simplify(b >= 0) is not sp.true:
            raise AssertionError(f"growing-channel logarithmic real gap is negative for j={j}: {b}")
        gap_at_R = simp(a + b / R)
        if sp.simplify(gap_at_R > 0) is not sp.true:
            raise AssertionError(f"growing-channel real gap not positive at tail for j={j}")
        gap_data.append((j, a, b, gap_at_R))

    minimum_gap_at_R = min(item[3] for item in gap_data)
    if sp.simplify(minimum_gap_at_R > 0) is not sp.true:
        raise AssertionError("minimum growing-channel tail gap is not positive")

    # Banach fixed-point estimate for q=e_g+Kq in the row 1-norm.
    deviation = simp(mass / (1 - mass))
    if sp.simplify(deviation <= sp.Rational(1, 15)) is not sp.true:
        raise AssertionError(f"growing-dual enclosure is weaker than expected: {deviation}")

    # For any exact transformed physical state Z_phys(R), the coefficient is
    # C_grow=exp(-phi_g(R))*q_g(R)Z_phys(R).  The positive scalar exponential
    # does not affect nonvanishing.  Holder duality gives
    # |(q_g-e_g^T)Z| <= ||q_g-e_g^T||_1 ||Z||_inf, yielding the finite-radius
    # sufficient test printed below.
    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_CGROW_DUAL_TAIL_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print("DIAGONAL_MODEL := Lambda(r)=D0+D1/r")
    print("INTEGRABLE_PERTURBATION := E(r)=D2/r^2+R_nf(r)")
    print(f"D2_INFINITY_NORM_UPPER := {sp.sstr(C2)}")
    print(f"NORMAL_FORM_R3_CONSTANT := {sp.sstr(C_nf)}")
    print(f"DUAL_TAIL_START := r >= {R}")
    print(f"VOLTERRA_MASS_BOUND := {sp.sstr(mass)} <= 1/16")
    print(f"GROWING_MODEL_MIN_REAL_GAP_AT_TAIL := {sp.sstr(minimum_gap_at_R)}")
    print("GROWING_DUAL_VOLTERRA_KERNEL := coordinatewise modulus <= 1 on the full row 1-norm")
    print("GROWING_DUAL_EXISTENCE := unique normalized adjoint row q_g with q_g(infinity)=e_g^T by contraction mapping")
    print(f"GROWING_DUAL_DEVIATION_BOUND := ||q_g-e_g^T||_1 <= {sp.sstr(deviation)} <= 1/15")
    print("CGROW_FINITE_RADIUS_IDENTITY := C_grow=exp(-phi_g(R))*q_g(R)*Z_phys(R)")
    print("CGROW_NONVANISHING_TEST := |Z_grow(R)| > deviation*||Z_phys(R)||_inf is sufficient")
    print("BOUNDARY := growing-channel dual tail enclosure certified; physical-state enclosure at the same radius and C_grow nonvanishing are not yet certified")


if __name__ == "__main__":
    main()
