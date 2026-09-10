#!/usr/bin/env python3
"""Certify the two-level constraint-adapted horizon blow-up.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The already-certified horizon-scaled six-state system is

    U_t = H(x) U,                 x=r-2,  t=log(x),

with a rank-one simple-pole residue supported in the last row,

    Res_{x=0} H = -(5/18) e_5 (e_0^T+e_4^T).

The physical leading scaled seed lies in the residue kernel U_0+U_4=0.
The first kinematic derivative of this constraint exposes the next leading
compatibility -2 U_0 + U_1 + U_5 = 0.  Introduce the exact two-level blow-up

    V_0=U_0, V_1=U_1, V_2=U_2, V_3=U_3,
    V_4=(U_0+U_4)/x,
    V_5=(-2 U_0+U_1+U_5)/x.

Equivalently U=P(x)V with det P=x^2.  Since d/dt=x d/dx,

    V_t = K(x)V,
    K=P^{-1}(H P - x P_x).

This verifier constructs K exactly and requires every simplified rational
entry to be regular at x=0.  It is a structural conditioning certificate
only: no interval propagation, r=4096 enclosure, or C_grow nonvanishing is
claimed.
"""
from __future__ import annotations

import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_horizon_scaled_log_system as scaled


def simp(value: sp.Expr) -> sp.Expr:
    return scaled.simp(value)


def matrix_simp(matrix: sp.Matrix) -> sp.Matrix:
    return scaled.matrix_simp(matrix)


def matrix_text(matrix: sp.Matrix) -> str:
    return scaled.matrix_text(matrix)


def build_scaled_generator() -> tuple[sp.Symbol, sp.Matrix]:
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
                raise AssertionError(
                    f"noninteger scaled-generator exponent at ({i},{j}): {exponent}"
                )
            H[i, j] = simp(x ** int(exponent) * G[i, j].subs(r, x + 2))
    for i in range(6):
        H[i, i] = simp(H[i, i] - powers[i])
    return x, matrix_simp(H)


def main() -> None:
    # Lock the immediate certified dependency and, in particular, the exact
    # residue classification that motivates this blow-up.
    dependency_buffer = io.StringIO()
    with contextlib.redirect_stdout(dependency_buffer):
        scaled.main()
    dependency_log = dependency_buffer.getvalue()
    required_tokens = [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_HORIZON_SCALED_LOG_SYSTEM_CERTIFIED",
        "HORIZON_SIMPLE_POLE_COUNT := 2",
        "HORIZON_SIMPLE_POLE_POSITIONS := [(5, 0), (5, 4)]",
        "HORIZON_RESIDUE_RANK := 1",
        "HORIZON_RESIDUE_MATRIX := [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-5/18, 0, 0, 0, -5/18, 0]]",
        "PHYSICAL_LEADING_SEED_RESIDUE := 0",
        "REGULAR_REMAINDER_HORIZON_POLE_COUNT := 0",
    ]
    for token in required_tokens:
        if token not in dependency_log:
            raise AssertionError("scaled-system dependency changed: " + token)

    x, H = build_scaled_generator()

    # U=P(x)V is the exact inverse of the two quotient definitions.
    P = sp.Matrix([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [-1, 0, 0, 0, x, 0],
        [2, -1, 0, 0, 0, x],
    ])
    P_inv = sp.Matrix([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [1/x, 0, 0, 0, 1/x, 0],
        [-2/x, 1/x, 0, 0, 0, 1/x],
    ])

    det_P = simp(P.det())
    if det_P != x**2:
        raise AssertionError(f"constraint blow-up determinant changed: {det_P}")
    if matrix_simp(P_inv * P - sp.eye(6)) != sp.zeros(6, 6):
        raise AssertionError("left inverse check P_inv*P=I failed")
    if matrix_simp(P * P_inv - sp.eye(6)) != sp.zeros(6, 6):
        raise AssertionError("right inverse check P*P_inv=I failed")

    # Exact log-time gauge transform: P_t=x*P_x.
    P_t = P.diff(x) * x
    K = matrix_simp(P_inv * (H * P - P_t))

    # Fail closed on any horizon pole after full exact simplification.
    horizon_poles: list[tuple[int, int, sp.Expr]] = []
    horizon_limit = sp.zeros(6, 6)
    nonzero_entry_count = 0
    for i in range(6):
        for j in range(6):
            value = simp(K[i, j])
            if value == 0:
                continue
            nonzero_entry_count += 1
            _num, den = sp.fraction(sp.together(value))
            den = sp.factor(den)
            den0 = simp(den.subs(x, 0))
            if den0 == 0:
                horizon_poles.append((i, j, den))
                continue
            horizon_limit[i, j] = simp(value.subs(x, 0))
    if horizon_poles:
        raise AssertionError(
            "constraint-adapted transformed generator retains horizon poles: "
            + sp.sstr(horizon_poles)
        )
    horizon_limit = matrix_simp(horizon_limit)

    # Pin the two exact quotient identities directly from P^{-1}U.
    U0, U1, U2, U3, U4, U5 = sp.symbols("U0 U1 U2 U3 U4 U5")
    U = sp.Matrix([U0, U1, U2, U3, U4, U5])
    V_from_U = matrix_simp(P_inv * U)
    expected = sp.Matrix([
        U0,
        U1,
        U2,
        U3,
        (U0 + U4) / x,
        (-2 * U0 + U1 + U5) / x,
    ])
    if matrix_simp(V_from_U - expected) != sp.zeros(6, 1):
        raise AssertionError("constraint quotient coordinate identities changed")

    # The physical leading scaled seed satisfies both numerator constraints.
    seed = sp.Matrix([
        1,
        sp.Rational(1, 2),
        sp.Rational(-1, 4),
        2,
        -1,
        sp.Rational(3, 2),
    ])
    first_constraint = simp(seed[0] + seed[4])
    second_constraint = simp(-2 * seed[0] + seed[1] + seed[5])
    if first_constraint != 0 or second_constraint != 0:
        raise AssertionError(
            f"physical leading seed constraint changed: first={first_constraint}, second={second_constraint}"
        )

    zeta = sp.symbols("zeta")
    characteristic = sp.factor(horizon_limit.charpoly(zeta).as_expr())

    # Algebraic equivalence of the transformed and untransformed differential
    # systems follows from invertibility of P for x>0 and the exact K formula.
    transform_residual = matrix_simp(P * K + P_t - H * P)
    if transform_residual != sp.zeros(6, 6):
        raise AssertionError("exact transformed-system equivalence residual is nonzero")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_HORIZON_CONSTRAINT_BLOWUP_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("HORIZON_VARIABLE := x=r-2")
    print("LOG_TIME := t=log(x)")
    print("INPUT_SCALED_STATE := U=(U0,U1,U2,U3,U4,U5)")
    print("BLOWUP_STATE := V=(U0,U1,U2,U3,(U0+U4)/x,(-2*U0+U1+U5)/x)")
    print("BLOWUP_INVERSE := U=(V0,V1,V2,V3,-V0+x*V4,2*V0-V1+x*V5)")
    print("BLOWUP_DETERMINANT := x^2")
    print("BLOWUP_INVERTIBILITY := exact for every x>0")
    print("PHYSICAL_LEADING_FIRST_CONSTRAINT := U0+U4=0")
    print("PHYSICAL_LEADING_SECOND_CONSTRAINT := -2*U0+U1+U5=0")
    print(f"REGULARIZED_GENERATOR_NONZERO_ENTRIES := {nonzero_entry_count}")
    print("REGULARIZED_HORIZON_POLE_COUNT := 0")
    print(f"REGULARIZED_HORIZON_LIMIT := {matrix_text(horizon_limit)}")
    print(f"REGULARIZED_HORIZON_CHARACTERISTIC := {sp.sstr(characteristic)}")
    print("EXACT_EQUIVALENCE := U=P(x)V and U_t=H(x)U iff V_t=K(x)V for every x>0")
    print("CONDITIONING_ROUTE := use the regularized V-system for validated near-horizon propagation, then transition to a finite-radius exterior representation")
    print("BOUNDARY := constraint-adapted regularization only; no validated interval propagation, no r=4096 physical-state enclosure, no Z_phys(4096) enclosure, no C_grow value/nonvanishing, and no global exceptional-mode closure claimed")


if __name__ == "__main__":
    main()
