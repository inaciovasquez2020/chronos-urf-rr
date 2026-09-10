#!/usr/bin/env python3
"""Certify a constraint-adapted near-horizon blow-up for the physical exterior state.

This verifier starts from the already-certified scaled logarithmic state

    U_t = H(x) U,    x=r-2, t=log x,

with H(x)=R/x+H_reg(x), where the exact rank-one residue is supported only
in row 5 and annihilates the physical leading scaled seed.

The first two vanishing constraint combinations are

    c = U0 + U4,
    d = -3/2 U0 + U1 + 1/2 U4 + U5.

For the physical Frobenius branch both vanish at leading order.  Introduce

    v = c/x,
    w = d/x,

and retain (U0,U1,U2,U3,v,w) as the new state V.  Equivalently U=Q(x)V
with a polynomial Q whose determinant is x^2 for x>0.  This verifier
constructs the transformed logarithmic generator

    M = Q^{-1}(H Q - x Q_x)

exactly and requires every entry to extend regularly to x=0.  It also pins
Q and the inverse coordinate formulas exactly.

This is a structural conditioning certificate only.  It performs no
validated numerical propagation and does not evaluate C_grow.
"""
from __future__ import annotations

import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_exterior_horizon_scaled_log_system as scaled


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def matrix_simp(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def matrix_text(matrix: sp.Matrix) -> str:
    return sp.sstr([[simp(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)])


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
                raise AssertionError(f"noninteger scaled exponent at {(i,j)}: {exponent}")
            H[i, j] = simp(x ** int(exponent) * G[i, j].subs(r, x + 2))
    for i in range(6):
        H[i, i] = simp(H[i, i] - powers[i])
    return x, matrix_simp(H)


def main() -> None:
    # Lock the immediate residue-classification dependency.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        scaled.main()
    dep = buffer.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_HORIZON_SCALED_LOG_SYSTEM_CERTIFIED",
        "HORIZON_SIMPLE_POLE_COUNT := 2",
        "HORIZON_RESIDUE_RANK := 1",
        "PHYSICAL_LEADING_SEED_RESIDUE := 0",
        "REGULAR_REMAINDER_HORIZON_POLE_COUNT := 0",
    ]:
        if token not in dep:
            raise AssertionError("scaled-residue dependency changed: " + token)

    x, H = build_scaled_generator()

    # V=(U0,U1,U2,U3,v,w), with
    # U4=x*v-U0 and U5=x*w+2*U0-U1-(x/2)*v.
    Q = sp.Matrix([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [-1, 0, 0, 0, x, 0],
        [2, -1, 0, 0, -x / 2, x],
    ])
    detQ = simp(Q.det())
    if detQ != x**2:
        raise AssertionError(f"unexpected blow-up determinant: {detQ}")

    # Exact inverse-coordinate identities.
    Qin = matrix_simp(Q.inv())
    expected_Qin = sp.Matrix([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [1/x, 0, 0, 0, 1/x, 0],
        [-sp.Rational(3,2)/x, 1/x, 0, 0, sp.Rational(1,2)/x, 1/x],
    ])
    if matrix_simp(Qin - expected_Qin) != sp.zeros(6, 6):
        raise AssertionError("constraint blow-up inverse formulas changed")

    Qt = matrix_simp(x * Q.diff(x))
    M = matrix_simp(Qin * (H * Q - Qt))

    poles: list[tuple[int, int, sp.Expr]] = []
    M0 = sp.zeros(6, 6)
    nonzero = 0
    for i in range(6):
        for j in range(6):
            value = simp(M[i, j])
            if value == 0:
                continue
            nonzero += 1
            _num, den = sp.fraction(sp.together(value))
            if simp(den.subs(x, 0)) == 0:
                poles.append((i, j, sp.factor(den)))
            else:
                M0[i, j] = simp(value.subs(x, 0))
    if poles:
        raise AssertionError(f"constraint-adapted generator retains horizon poles: {poles}")
    M0 = matrix_simp(M0)

    # Pin the coordinate meanings directly.
    U = sp.symbols("U0:6")
    Uvec = sp.Matrix(U)
    VfromU = matrix_simp(Qin * Uvec)
    if simp(VfromU[4] - (U[0] + U[4]) / x) != 0:
        raise AssertionError("v coordinate identity failed")
    d = -sp.Rational(3, 2) * U[0] + U[1] + sp.Rational(1, 2) * U[4] + U[5]
    if simp(VfromU[5] - d / x) != 0:
        raise AssertionError("w coordinate identity failed")

    zeta = sp.symbols("zeta")
    char0 = sp.factor(M0.charpoly(zeta).as_expr())

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_CONSTRAINT_BLOWUP_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("BASE_SCALED_STATE := U=(U0,U1,U2,U3,U4,U5)")
    print("BLOWUP_STATE := V=(U0,U1,U2,U3,v,w)")
    print("FIRST_CONSTRAINT := c=U0+U4")
    print("SECOND_CONSTRAINT := d=-3/2*U0+U1+1/2*U4+U5")
    print("BLOWUP_COORDINATES := v=c/x; w=d/x")
    print("INVERSE_COORDINATES := U4=x*v-U0; U5=x*w+2*U0-U1-(x/2)*v")
    print("BLOWUP_MATRIX_DETERMINANT := x^2")
    print(f"CONSTRAINT_ADAPTED_GENERATOR_NONZERO_ENTRIES := {nonzero}")
    print("CONSTRAINT_ADAPTED_HORIZON_POLE_COUNT := 0")
    print(f"CONSTRAINT_ADAPTED_HORIZON_LIMIT := {matrix_text(M0)}")
    print(f"CONSTRAINT_ADAPTED_HORIZON_CHARACTERISTIC := {sp.sstr(char0)}")
    print("EXACT_EQUIVALENCE := U=Q(x)V and U_t=H(x)U iff V_t=M(x)V for every x>0")
    print("CONDITIONING_ROUTE := use V for validated near-horizon propagation, then convert to a standard exterior state away from x=0")
    print("BOUNDARY := regularized structural system only; no validated propagation to r=4096, no Z_phys(4096) enclosure, no C_grow value/nonvanishing, and no global exceptional-mode closure claimed")


if __name__ == "__main__":
    main()
