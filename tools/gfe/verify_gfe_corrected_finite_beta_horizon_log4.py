#!/usr/bin/env python3
"""Audit the minimal log^4 generalized Frobenius chain at the finite-beta horizon resonance.

This verifier reuses the exact action-derived weighted horizon matrix from
verify_gfe_corrected_finite_beta_horizon_indicial.py.  At the physical ingoing
exponent p=-2 i M omega, the n=1 shifted indicial matrix vanishes and L'(q*) has
rank one.  Pure-power through minimal log^3 continuations are already known to
leave the same one-dimensional quotient obstruction.

For

    x^(p+1) [c4 log^4 x + c3 log^3 x + c2 log^2 x + c1 log x + c0],

the exact n=1 equations are

    4 L'(q*) c4 = 0,
    6 L''(q*) c4 + 3 L'(q*) c3 = 0,
    4 L'''(q*) c4 + 3 L''(q*) c3 + 2 L'(q*) c2 = 0,
    R1 + L''''(q*) c4 + L'''(q*) c3 + L''(q*) c2 + L'(q*) c1 = 0.

The script checks whether L'''' supplies the first new quotient direction.  It
also records whether L^(5) vanishes, which identifies whether any still-higher
logarithmic analysis can introduce a genuinely new derivative of the indicial
matrix (without claiming that higher chains are automatically closed).
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
    L4 = base._simplified_matrix(leading.diff(p, 4).subs(p, resonant_exponent))
    L5 = base._simplified_matrix(leading.diff(p, 5).subs(p, resonant_exponent))

    if base._is_zero_matrix(L1) or sp.factor(sp.cancel(L1.det())) != 0:
        raise AssertionError("expected nonzero rank-one L'(q*) matrix")

    left_null = sp.Matrix([omega, 2 * M * omega - I])
    if not base._is_zero_matrix(base._simplified_matrix(left_null.T * L1)):
        raise AssertionError("left-null vector for L'(q*) changed")

    c4 = base._simplified_matrix(base._right_kernel_vector(L1))
    if not base._is_zero_matrix(base._simplified_matrix(4 * L1 * c4)):
        raise AssertionError("constructed log^4 top coefficient violates log^3 equation")

    # log^2 equation: 6 L2 c4 + 3 L1 c3 = 0.
    log2_target = base._simplified_matrix(-2 * L2 * c4)
    log2_pairing = sp.factor(sp.cancel((left_null.T * log2_target)[0]))
    if log2_pairing != 0:
        raise AssertionError(
            "log^4 log^2 equation is not solvable in im L'; "
            f"pairing={sp.sstr(log2_pairing)}"
        )
    c3 = _rank_one_preimage(L1, log2_target)
    log2_residual = base._simplified_matrix(6 * L2 * c4 + 3 * L1 * c3)
    if not base._is_zero_matrix(log2_residual):
        raise AssertionError(
            "constructed c3 does not solve log^2 equation; "
            f"residual={log2_residual.tolist()}"
        )

    # log equation: 4 L3 c4 + 3 L2 c3 + 2 L1 c2 = 0.
    log1_source = base._simplified_matrix(4 * L3 * c4 + 3 * L2 * c3)
    log1_pairing = sp.factor(sp.cancel((left_null.T * log1_source)[0]))
    if log1_pairing != 0:
        raise AssertionError(
            "log^4 log equation is obstructed before the constant equation; "
            f"pairing={sp.sstr(log1_pairing)}"
        )
    c2 = _rank_one_preimage(
        L1,
        base._simplified_matrix(-sp.Rational(1, 2) * log1_source),
    )
    log1_residual = base._simplified_matrix(
        4 * L3 * c4 + 3 * L2 * c3 + 2 * L1 * c2
    )
    if not base._is_zero_matrix(log1_residual):
        raise AssertionError(
            "constructed c2 does not solve log equation; "
            f"residual={log1_residual.tolist()}"
        )

    unit_log4_constant_lift = base._simplified_matrix(
        L4 * c4 + L3 * c3 + L2 * c2
    )
    log4_quotient_pairing = sp.factor(
        sp.cancel((left_null.T * unit_log4_constant_lift)[0])
    )
    source_quotient_pairing = sp.factor(
        sp.cancel((left_null.T * first_residual)[0])
    )

    print("GFE_CORRECTED_FINITE_BETA_HORIZON_LOG4_AUDIT")
    print("PHYSICAL_INGOING_EXPONENT := -2*I*M*omega")
    print("RESONANT_EXPONENT := 1 - 2*I*M*omega")
    print("LOG4_TOP_COEFFICIENT_KERNEL := [" + ", ".join(sp.sstr(v) for v in c4) + "]")
    print("LOG4_LOG2_EQUATION := solved exactly")
    print("LOG4_LOG1_EQUATION := solved exactly")
    print("LOG4_UNIT_QUOTIENT_PAIRING := " + sp.sstr(log4_quotient_pairing))
    print("N1_SOURCE_QUOTIENT_PAIRING := " + sp.sstr(source_quotient_pairing))
    print("INDICIAL_FIFTH_DERIVATIVE_ZERO := " + str(base._is_zero_matrix(L5)))

    if log4_quotient_pairing == 0:
        if source_quotient_pairing == 0:
            raise AssertionError(
                "both source and log^4 quotient pairings vanished identically; "
                "classification lost its generic obstruction diagnostic"
            )
        print("LOG4_FINITE_BETA_FROBENIUS := cannot change the quotient obstruction")
        print(
            "NEXT_ROUTE := analyze the exceptional omega=I/(4*M) sector or prove a higher-log structural induction"
        )
        return

    scale = sp.factor(sp.cancel(-source_quotient_pairing / log4_quotient_pairing))
    C4 = base._simplified_matrix(scale * c4)
    C3 = base._simplified_matrix(scale * c3)
    C2 = base._simplified_matrix(scale * c2)

    scaled_log2 = base._simplified_matrix(6 * L2 * C4 + 3 * L1 * C3)
    scaled_log1 = base._simplified_matrix(4 * L3 * C4 + 3 * L2 * C3 + 2 * L1 * C2)
    if not base._is_zero_matrix(scaled_log2) or not base._is_zero_matrix(scaled_log1):
        raise AssertionError("scaled log^4 chain violates upper logarithmic equations")

    constant_after_log4 = base._simplified_matrix(
        first_residual + L4 * C4 + L3 * C3 + L2 * C2
    )
    remaining_pairing = sp.factor(
        sp.cancel((left_null.T * constant_after_log4)[0])
    )
    if remaining_pairing != 0:
        raise AssertionError(
            "log^4 quotient cancellation failed; "
            f"pairing={sp.sstr(remaining_pairing)}"
        )

    C1 = _rank_one_preimage(L1, -constant_after_log4)
    full_constant_residual = base._simplified_matrix(
        first_residual + L4 * C4 + L3 * C3 + L2 * C2 + L1 * C1
    )
    if not base._is_zero_matrix(full_constant_residual):
        raise AssertionError(
            "log^4 generalized chain failed exact n=1 cancellation; "
            f"residual={full_constant_residual.tolist()}"
        )

    print("LOG4_SCALE := " + sp.sstr(scale))
    print("MINIMAL_LOG4_N1_CHAIN := exact cancellation verified")
    print("NEXT_ROUTE := test horizon admissibility of the forced log^4 branch")


if __name__ == "__main__":
    main()
