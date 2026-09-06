#!/usr/bin/env python3
"""Audit the minimal log^3 generalized Frobenius chain at the finite-beta horizon resonance.

This verifier reuses the exact action-derived weighted horizon matrix from
verify_gfe_corrected_finite_beta_horizon_indicial.py.  At the physical ingoing
exponent p=-2 i M omega, the n=1 shifted indicial matrix vanishes, while L'(q*)
has rank one.  Pure-power, one-log, and minimal log^2 continuations are already
known to leave a one-dimensional quotient obstruction.

For the minimal log^3 correction

    x^(p+1) [c3 log^3 x + c2 log^2 x + c1 log x + c0],

the exact equations at n=1 are

    3 L'(q*) c3 = 0,
    3 L''(q*) c3 + 2 L'(q*) c2 = 0,
    R1 + L'''(q*) c3 + L''(q*) c2 + L'(q*) c1 = 0.

The script determines symbolically whether this is the first logarithmic level
that can change the quotient obstruction.  It fails only if the algebraic
identities used in the classification are inconsistent.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


def _rank_one_preimage(matrix: sp.Matrix, target: sp.Matrix) -> sp.Matrix:
    """Return one exact preimage of target under a nonzero rank-one 2x2 matrix."""
    for column_index in range(matrix.cols):
        column = matrix[:, column_index]
        for row_index in range(matrix.rows):
            pivot = sp.factor(sp.cancel(column[row_index]))
            if pivot == 0:
                continue
            scale = sp.factor(sp.cancel(target[row_index] / pivot))
            candidate = sp.zeros(matrix.cols, 1)
            candidate[column_index, 0] = scale
            residual = base._simplified_matrix(matrix * candidate - target)
            if base._is_zero_matrix(residual):
                return base._simplified_matrix(candidate)
    raise AssertionError(
        "target is not in the image of the rank-one logarithmic correction matrix"
    )


def main() -> None:
    _, leading, subleading, _ = base.derive_weighted_horizon_frobenius_system()

    M = base.M
    beta = base.beta
    lam = base.lam
    omega = base.omega
    p = base.p
    I = base.I

    physical_exponent = -2 * I * M * omega
    resonant_exponent = physical_exponent + 1
    seed = sp.Matrix([1, 2 * M])

    first_residual = base._simplified_matrix(
        subleading.subs(p, physical_exponent) * seed
    )

    L1 = base._simplified_matrix(leading.diff(p).subs(p, resonant_exponent))
    L2 = base._simplified_matrix(leading.diff(p, 2).subs(p, resonant_exponent))
    L3 = base._simplified_matrix(leading.diff(p, 3).subs(p, resonant_exponent))

    if base._is_zero_matrix(L1) or sp.factor(sp.cancel(L1.det())) != 0:
        raise AssertionError("expected nonzero rank-one L'(q*) matrix")

    left_null = sp.Matrix([omega, 2 * M * omega - I])
    if not base._is_zero_matrix(base._simplified_matrix(left_null.T * L1)):
        raise AssertionError("left-null vector for L'(q*) changed")

    c3_kernel = base._simplified_matrix(base._right_kernel_vector(L1))
    if not base._is_zero_matrix(base._simplified_matrix(L1 * c3_kernel)):
        raise AssertionError("constructed log^3 top coefficient is not in ker L'")

    # The log equation 3 L'' c3 + 2 L' c2 = 0 must be solvable first.
    L2_c3 = base._simplified_matrix(L2 * c3_kernel)
    L2_c3_pairing = sp.factor(sp.cancel((left_null.T * L2_c3)[0]))
    if L2_c3_pairing != 0:
        raise AssertionError(
            "known log^2 image containment changed before log^3 audit; "
            f"pairing={sp.sstr(L2_c3_pairing)}"
        )

    c2_base = _rank_one_preimage(
        L1,
        base._simplified_matrix(-sp.Rational(3, 2) * L2_c3),
    )
    log_equation_residual = base._simplified_matrix(
        3 * L2_c3 + 2 * L1 * c2_base
    )
    if not base._is_zero_matrix(log_equation_residual):
        raise AssertionError(
            "constructed log^3/log^2 coefficients do not solve the log equation; "
            f"residual={log_equation_residual.tolist()}"
        )

    # This is the new quotient direction available at log^3.
    unit_log3_constant_lift = base._simplified_matrix(
        L3 * c3_kernel + L2 * c2_base
    )
    log3_quotient_pairing = sp.factor(
        sp.cancel((left_null.T * unit_log3_constant_lift)[0])
    )
    source_quotient_pairing = sp.factor(
        sp.cancel((left_null.T * first_residual)[0])
    )

    print("GFE_CORRECTED_FINITE_BETA_HORIZON_LOG3_AUDIT")
    print("PHYSICAL_INGOING_EXPONENT := -2*I*M*omega")
    print("RESONANT_EXPONENT := 1 - 2*I*M*omega")
    print("LOG3_TOP_COEFFICIENT_KERNEL := [" + ", ".join(sp.sstr(v) for v in c3_kernel) + "]")
    print("LOG3_LOG_EQUATION := solved exactly")
    print("LOG3_UNIT_QUOTIENT_PAIRING := " + sp.sstr(log3_quotient_pairing))
    print("N1_SOURCE_QUOTIENT_PAIRING := " + sp.sstr(source_quotient_pairing))

    if log3_quotient_pairing == 0:
        if source_quotient_pairing == 0:
            raise AssertionError(
                "both source and log^3 quotient pairings vanished identically; "
                "classification lost its generic obstruction diagnostic"
            )
        print("LOG3_FINITE_BETA_FROBENIUS := cannot change the quotient obstruction")
        print("NEXT_ROUTE := test log^4 generalized Frobenius chain or exceptional-frequency sector")
        return

    scale = sp.factor(sp.cancel(-source_quotient_pairing / log3_quotient_pairing))
    c3 = base._simplified_matrix(scale * c3_kernel)
    c2 = base._simplified_matrix(scale * c2_base)

    scaled_log_residual = base._simplified_matrix(3 * L2 * c3 + 2 * L1 * c2)
    if not base._is_zero_matrix(scaled_log_residual):
        raise AssertionError(
            "scaled log^3 coefficients violate the log equation; "
            f"residual={scaled_log_residual.tolist()}"
        )

    constant_after_log3 = base._simplified_matrix(
        first_residual + L3 * c3 + L2 * c2
    )
    remaining_pairing = sp.factor(
        sp.cancel((left_null.T * constant_after_log3)[0])
    )
    if remaining_pairing != 0:
        raise AssertionError(
            "log^3 quotient cancellation failed; "
            f"pairing={sp.sstr(remaining_pairing)}"
        )

    c1 = _rank_one_preimage(L1, -constant_after_log3)
    full_constant_residual = base._simplified_matrix(
        first_residual + L3 * c3 + L2 * c2 + L1 * c1
    )
    if not base._is_zero_matrix(full_constant_residual):
        raise AssertionError(
            "log^3 generalized chain failed exact n=1 cancellation; "
            f"residual={full_constant_residual.tolist()}"
        )

    print("LOG3_SCALE := " + sp.sstr(scale))
    print("LOG3_COEFFICIENT := [" + ", ".join(sp.sstr(v) for v in c3) + "]")
    print("LOG2_COEFFICIENT := [" + ", ".join(sp.sstr(v) for v in c2) + "]")
    print("LOG1_COEFFICIENT := [" + ", ".join(sp.sstr(v) for v in c1) + "]")
    print("MINIMAL_LOG3_N1_CHAIN := exact cancellation verified")
    print("NEXT_ROUTE := test horizon admissibility of the forced log^3 branch before horizon-to-r_c propagation")


if __name__ == "__main__":
    main()
