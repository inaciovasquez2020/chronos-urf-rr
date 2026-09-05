#!/usr/bin/env python3
"""Certify the all-finite-log obstruction at the finite-beta n=1 horizon resonance.

Let q* = 1 - 2 i M omega and let

    H(z) = L(q* + z),

where L is the exact action-derived weighted horizon indicial matrix.  The n=1
resonance is H(0)=0.  A finite generalized Frobenius correction

    x^q* P(log x)

with vector-valued polynomial P is acted on by H(D), D=d/d(log x).  Thus the
inhomogeneous n=1 problem is H(D)P=-R1.

The exact shifted indicial pencil has the primitive polynomial left syzygy

    W(z)^T = (omega, 2 M omega - i + i z),
    W(z)^T H(z) = 0.

Therefore W(D)^T H(D)P=0 for every finite vector polynomial P.  Since R1 is
constant in log(x), all positive powers of D in W(D) annihilate it and

    W(D)^T R1 = W(0)^T R1
              = -5 beta^2 lambda(lambda-2)(4 M omega-i)/(288 M^5).

Hence no finite polynomial in log(x), of any degree, can solve the n=1
resonant correction when beta*lambda*(lambda-2)*(4 M omega-i) != 0.  This is
an all-finite-log result, not an extrapolation from log^1 through log^4.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


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

    # Primitive syzygy: the previous column construction contains only removable
    # scalar/polynomial content.  This content-free representative specializes
    # exactly to the known one-log left-null vector at z=0.
    W = sp.Matrix([omega, 2 * M * omega - I + I * z])
    syzygy_residual = base._simplified_matrix(W.T * H)
    if not base._is_zero_matrix(syzygy_residual):
        raise AssertionError(
            "primitive polynomial left syzygy does not annihilate H(z); "
            f"residual={syzygy_residual.tolist()}"
        )

    W0 = base._simplified_matrix(W.subs(z, 0))
    expected_W0 = sp.Matrix([omega, 2 * M * omega - I])
    if not base._is_zero_matrix(base._simplified_matrix(W0 - expected_W0)):
        raise AssertionError(
            "primitive syzygy no longer specializes to the known one-log left-null vector"
        )

    L1 = base._simplified_matrix(leading.diff(p).subs(p, resonant_exponent))
    if not base._is_zero_matrix(base._simplified_matrix(W0.T * L1)):
        raise AssertionError("W(0) is not a left-null vector of L'(q*)")

    first_residual = base._simplified_matrix(
        subleading.subs(p, physical_exponent) * seed
    )
    source_pairing = sp.factor(sp.cancel((W0.T * first_residual)[0]))
    expected_pairing = sp.factor(
        -5
        * beta**2
        * lam
        * (lam - 2)
        * (4 * M * omega - I)
        / (288 * M**5)
    )
    if sp.factor(sp.cancel(source_pairing - expected_pairing)) != 0:
        raise AssertionError(
            "primitive all-finite-log source pairing changed; "
            f"actual={sp.sstr(source_pairing)}, expected={sp.sstr(expected_pairing)}"
        )

    # Constant-coefficient symbol calculus: polynomial multiplication
    # W(z)^T H(z)=0 is exactly operator composition W(D)^T H(D)=0.  For a
    # constant source R1, W(D)^T R1=W(0)^T R1.  Therefore a nonzero pairing is
    # an obstruction for every finite-degree polynomial P(log x), irrespective
    # of the degree of P.

    flagship_pairing = sp.factor(sp.cancel(source_pairing.subs(lam, 6)))
    exceptional_pairing = sp.factor(
        sp.cancel(source_pairing.subs(omega, I / (4 * M)))
    )
    gr_pairing = sp.factor(sp.cancel(source_pairing.subs(beta, 0)))
    if exceptional_pairing != 0:
        raise AssertionError("primitive syzygy obstruction did not vanish at omega=I/(4*M)")
    if gr_pairing != 0:
        raise AssertionError("primitive syzygy obstruction did not vanish in the GR beta=0 limit")

    print("GFE_CORRECTED_FINITE_BETA_HORIZON_ALL_FINITE_LOGS_CERTIFIED")
    print("RESONANT_PENCIL := H(z)=L(1-2*I*M*omega+z)")
    print("PRIMITIVE_POLYNOMIAL_LEFT_SYZYGY := [omega, 2*M*omega-I+I*z]")
    print("SYZYGY_AT_ZERO := [omega, 2*M*omega-I]")
    print("SOURCE_SYZYGY_PAIRING := " + sp.sstr(source_pairing))
    print("FLAGSHIP_ELL2_SOURCE_SYZYGY_PAIRING := " + sp.sstr(flagship_pairing))
    print("ALL_FINITE_LOG_POLYNOMIALS := obstructed when beta*lambda*(lambda-2)*(4*M*omega-I) != 0")
    print("EXCEPTIONAL_FREQUENCY := omega=I/(4*M) remains open")
    print("GR_LIMIT_BETA_ZERO := obstruction vanishes")
    print("NEXT_ROUTE := analyze the exceptional omega=I/(4*M) sector")


if __name__ == "__main__":
    main()
