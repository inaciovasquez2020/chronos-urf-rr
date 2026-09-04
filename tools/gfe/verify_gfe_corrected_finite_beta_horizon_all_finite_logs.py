#!/usr/bin/env python3
"""Certify the all-finite-log obstruction at the finite-beta n=1 horizon resonance.

Let q* = 1 - 2 i M omega and let

    H(z) = L(q* + z),

where L is the exact action-derived weighted horizon indicial matrix.  The n=1
resonance is H(0)=0.  A finite generalized Frobenius correction

    x^q* P(log x)

with vector-valued polynomial P is acted on by the constant-coefficient matrix
differential operator H(D), D=d/d(log x).  Thus the inhomogeneous n=1 problem
is

    H(D) P = -R1.

Because det H(z) vanishes identically, H admits a polynomial left syzygy
W(z)^T H(z)=0.  After dividing the common z factor from a nonzero column, W(0)
is a nonzero left-null vector of H'(0)=L'(q*).  Therefore

    W(D)^T H(D) P = 0

for every polynomial P, while for the constant source R1,

    W(D)^T R1 = W(0)^T R1.

The verifier proves that this constant is a nonzero rational multiple of the
previously certified quotient obstruction

    -5 beta^2 lambda(lambda-2)(4 M omega-i)/(288 M^5).

Hence no finite polynomial in log(x), of any degree, can solve the n=1
resonant correction when beta*lambda*(lambda-2)*(4 M omega-i) != 0.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


def _column_reduced_by_resonant_factor(H: sp.Matrix, z: sp.Symbol) -> tuple[int, sp.Matrix]:
    """Find a column whose exact common resonant factor z can be removed."""
    for column_index in range(H.cols):
        column = H[:, column_index]
        if base._is_zero_matrix(column):
            continue
        reduced_entries = []
        divisible = True
        for entry in column:
            quotient = sp.factor(sp.cancel(entry / z))
            if sp.factor(sp.cancel(entry - z * quotient)) != 0:
                divisible = False
                break
            reduced_entries.append(quotient)
        if not divisible:
            continue
        reduced = base._simplified_matrix(sp.Matrix(reduced_entries))
        reduced_at_zero = base._simplified_matrix(reduced.subs(z, 0))
        if not base._is_zero_matrix(reduced_at_zero):
            return column_index, reduced
    raise AssertionError("no nonzero indicial column had the expected simple resonant z factor")


def _proportionality_scale(v: sp.Matrix, reference: sp.Matrix) -> sp.Expr:
    """Return exact scalar a with v=a*reference, or fail."""
    cross = sp.factor(sp.cancel(v[0] * reference[1] - v[1] * reference[0]))
    if cross != 0:
        raise AssertionError(
            "primitive polynomial syzygy at z=0 is not proportional to the known left-null vector; "
            f"cross={sp.sstr(cross)}"
        )
    for index in range(2):
        if sp.factor(sp.cancel(reference[index])) == 0:
            continue
        scale = sp.factor(sp.cancel(v[index] / reference[index]))
        residual = base._simplified_matrix(v - scale * reference)
        if base._is_zero_matrix(residual):
            return scale
    raise AssertionError("could not normalize polynomial syzygy against known left-null vector")


def main() -> None:
    _, leading, subleading, _ = base.derive_weighted_horizon_frobenius_system()

    M = base.M
    beta = base.beta
    lam = base.lam
    omega = base.omega
    p = base.p
    I = base.I
    z = sp.Symbol("z")

    physical_exponent = -2 * I * M * omega
    resonant_exponent = physical_exponent + 1
    seed = sp.Matrix([1, 2 * M])

    H = base._simplified_matrix(leading.subs(p, resonant_exponent + z))
    if not base._is_zero_matrix(base._simplified_matrix(H.subs(z, 0))):
        raise AssertionError("shifted indicial pencil no longer vanishes at the n=1 resonance")

    determinant = sp.factor(sp.cancel(H.det()))
    if determinant != 0:
        raise AssertionError(
            "shifted indicial pencil lost its exact rank-one identity; "
            f"det={sp.sstr(determinant)}"
        )

    column_index, reduced_column = _column_reduced_by_resonant_factor(H, z)
    W = base._simplified_matrix(sp.Matrix([-reduced_column[1], reduced_column[0]]))
    syzygy_residual = base._simplified_matrix(W.T * H)
    if not base._is_zero_matrix(syzygy_residual):
        raise AssertionError(
            "constructed polynomial left syzygy does not annihilate H(z); "
            f"residual={syzygy_residual.tolist()}"
        )

    W0 = base._simplified_matrix(W.subs(z, 0))
    if base._is_zero_matrix(W0):
        raise AssertionError("primitive polynomial syzygy vanished at z=0")

    L1 = base._simplified_matrix(leading.diff(p).subs(p, resonant_exponent))
    if not base._is_zero_matrix(base._simplified_matrix(W0.T * L1)):
        raise AssertionError("W(0) is not a left-null vector of L'(q*)")

    known_left_null = sp.Matrix([omega, 2 * M * omega - I])
    normalization = _proportionality_scale(W0, known_left_null)
    if sp.factor(sp.cancel(normalization)) == 0:
        raise AssertionError("polynomial syzygy normalization unexpectedly vanished")

    first_residual = base._simplified_matrix(
        subleading.subs(p, physical_exponent) * seed
    )
    source_pairing = sp.factor(sp.cancel((W0.T * first_residual)[0]))
    known_pairing = sp.factor(
        -5
        * beta**2
        * lam
        * (lam - 2)
        * (4 * M * omega - I)
        / (288 * M**5)
    )
    expected_pairing = sp.factor(sp.cancel(normalization * known_pairing))
    if sp.factor(sp.cancel(source_pairing - expected_pairing)) != 0:
        raise AssertionError(
            "all-finite-log syzygy pairing changed; "
            f"actual={sp.sstr(source_pairing)}, expected={sp.sstr(expected_pairing)}"
        )

    # Constant-coefficient symbol calculus: polynomial multiplication of W(z)^T
    # and H(z) is exactly the composition W(D)^T H(D).  The exact zero syzygy
    # above therefore annihilates H(D)P for every vector polynomial P.  Since R1
    # is constant in log(x), all positive powers of D in W(D) kill it and only
    # W(0)^T R1 remains.  A generically nonzero source_pairing is therefore an
    # all-degree obstruction, not a finite-depth extrapolation.

    flagship_pairing = sp.factor(sp.cancel(source_pairing.subs(lam, 6)))
    exceptional_pairing = sp.factor(
        sp.cancel(source_pairing.subs(omega, I / (4 * M)))
    )
    gr_pairing = sp.factor(sp.cancel(source_pairing.subs(beta, 0)))
    if exceptional_pairing != 0:
        raise AssertionError("syzygy obstruction did not vanish in exceptional frequency sector")
    if gr_pairing != 0:
        raise AssertionError("syzygy obstruction did not vanish in the GR beta=0 limit")

    print("GFE_CORRECTED_FINITE_BETA_HORIZON_ALL_FINITE_LOGS_CERTIFIED")
    print("RESONANT_PENCIL := H(z)=L(1-2*I*M*omega+z)")
    print(f"PRIMITIVE_SYZYGY_COLUMN := {column_index}")
    print("POLYNOMIAL_LEFT_SYZYGY := [" + ", ".join(sp.sstr(v) for v in W) + "]")
    print("SYZYGY_AT_ZERO := [" + ", ".join(sp.sstr(v) for v in W0) + "]")
    print("SYZYGY_NORMALIZATION_TO_KNOWN_LEFT_NULL := " + sp.sstr(normalization))
    print("SOURCE_SYZYGY_PAIRING := " + sp.sstr(source_pairing))
    print("FLAGSHIP_ELL2_SOURCE_SYZYGY_PAIRING := " + sp.sstr(flagship_pairing))
    print("ALL_FINITE_LOG_POLYNOMIALS := obstructed when beta*lambda*(lambda-2)*(4*M*omega-I) != 0")
    print("EXCEPTIONAL_FREQUENCY := omega=I/(4*M) remains open")
    print("GR_LIMIT_BETA_ZERO := obstruction vanishes")
    print("NEXT_ROUTE := analyze the exceptional omega=I/(4*M) sector")


if __name__ == "__main__":
    main()
