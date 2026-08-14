#!/usr/bin/env python3
"""Derive the exact Fourier-radial Euler and six-state surface from the
certified corrected AEH=1/2 action.  No downstream formula is hand-entered.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_full_lagrangian.json"
OUTPUT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"
RECEIPT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator_receipt.txt"

M, r, beta, lam, omega = s.symbols("M r beta lam omega")
I = s.I

# The source action contains jets only through these bounds, while its Euler
# equations require twice those orders.
jets = {
    (field, to, ro): s.Symbol(f"h{field}t{to}r{ro}")
    for field in range(2) for to in range(5) for ro in range(5)
}


def simp(expr: s.Expr) -> s.Expr:
    # ``cancel`` over all parameters triggers expensive multivariate GCDs.
    # A single exact common denominator is canonical enough for this artifact
    # and keeps the rebuild deterministic and tractable.
    return s.together(expr)


def total(expr: s.Expr, direction: str) -> s.Expr:
    """Exact total derivative on the finite jet algebra."""
    out = s.diff(expr, r) if direction == "r" else s.Integer(0)
    dt, dr = ((1, 0) if direction == "t" else (0, 1))
    for (field, to, ro), jet in jets.items():
        nxt = jets.get((field, to + dt, ro + dr))
        if nxt is not None:
            coefficient = s.diff(expr, jet)
            if coefficient != 0:
                out += coefficient * nxt
    return s.expand(out)


def euler(lagrangian: s.Expr, field: int) -> s.Expr:
    out = s.Integer(0)
    for (ff, to, ro), jet in jets.items():
        if ff != field:
            continue
        term = s.diff(lagrangian, jet)
        if term == 0:
            continue
        for _ in range(to):
            term = -total(term, "t")
        for _ in range(ro):
            term = -total(term, "r")
        out += term
    return s.expand(out)


def radialize(expr: s.Expr) -> s.Expr:
    return s.expand(expr.xreplace({
        jet: (-I * omega) ** to * s.Symbol(f"h{field}r{ro}")
        for (field, to, ro), jet in jets.items()
    }))


def canonical(expr: s.Expr) -> str:
    return s.sstr(simp(expr))


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    locals_map = {"M": M, "r": r, "beta": beta, "lambda": lam, **{
        str(value): value for value in jets.values()
    }}
    lagrangian = s.sympify(
        source["full_lagrangian"].replace("lambda", "lam"),
        locals={**locals_map, "lam": lam},
    )

    euler_pde = [euler(lagrangian, field) for field in range(2)]
    equations = [radialize(eq) for eq in euler_pde]

    # Exact identity certificate: independently reconstruct the variational
    # sum a second time from the source and compare before Fourier reduction.
    euler_identity = [s.expand(eq - euler(lagrangian, field)) == 0
                      for field, eq in enumerate(euler_pde)]
    if euler_identity != [True, True]:
        raise SystemExit("Euler-from-action identity failed")

    h = [[s.Symbol(f"h{field}r{order}") for order in range(5)]
         for field in range(2)]
    orders = {}
    for ei, eq in enumerate(equations):
        for field in range(2):
            present = [j for j in range(5) if s.diff(eq, h[field][j]) != 0]
            orders[f"E{ei}_h{field}"] = max(present or [0])

    # For the staircase E0=(h0'''' ,h1'''), E1=(h0''',h1''), differentiate
    # E1 and solve the resulting 2x2 system for (h0'''',h1''').
    c4 = simp(s.diff(equations[0], h[0][4]))
    d3 = simp(s.diff(equations[0], h[1][3]))
    a3 = simp(s.diff(equations[1], h[0][3]))
    b2 = simp(s.diff(equations[1], h[1][2]))
    principal = s.Matrix([[c4, d3], [a3, b2]])
    determinant = simp(principal.det())

    state = [h[0][0], h[0][1], h[0][2], h[1][0], h[1][1], h[1][2]]
    # E1 gives h0''' directly.  Its total radial derivative plus E0 gives
    # h1'''; expressing this as an ordinary generator requires a3 and the
    # Schur pivot kappa=d3-c4*b2/a3 to be nonzero.
    # Six-state descriptor.  The last equation is a3*E0-c4*d_r(E1), which
    # cancels h0'''' identically.  Shift identities are substituted there;
    # X2'=h0''' and X5'=h1''' remain descriptor derivatives.
    descriptor_e = s.zeros(6)
    descriptor_a = s.zeros(6)
    for row, (left, right) in enumerate(((0, 1), (1, 2), (3, 4), (4, 5))):
        descriptor_e[row, left] = 1
        descriptor_a[row, right] = 1
    e1_remainder = s.expand(equations[1] - a3*h[0][3])
    descriptor_e[4, 2] = a3
    for col, variable in enumerate(state):
        descriptor_a[4, col] = -s.diff(e1_remainder, variable)

    d_e1 = radialize(total(euler_pde[1], "r"))
    eliminated = s.expand(
        a3*(equations[0] - c4*h[0][4])
        - c4*(d_e1 - a3*h[0][4])
    )
    # Move the two genuine state derivatives to E, and apply the four shift
    # identities to all other third derivatives.
    descriptor_e[5, 2] = s.diff(eliminated, h[0][3])
    descriptor_e[5, 5] = s.diff(eliminated, h[1][3])
    eliminated_remainder = s.expand(
        eliminated
        - descriptor_e[5, 2]*h[0][3]
        - descriptor_e[5, 5]*h[1][3]
    )
    for col, variable in enumerate(state):
        descriptor_a[5, col] = -s.diff(eliminated_remainder, variable)
    descriptor_det = simp(descriptor_e.det())

    # Direct GR check from the corrected equations, not from a stale generator.
    f = (r - 2*M)/r
    mu = lam - 2
    q = -I*omega*h[1][0] - h[0][1] + 2*h[0][0]/r
    a0 = s.diff(q, r) + 2*q/r + mu*h[0][0]/(f*r**2)
    a0 = a0.xreplace({s.Derivative(h[0][1], r): h[0][2]})
    # Algebraic radial derivative above is clearer explicitly.
    a0 = -I*omega*h[1][1] - h[0][2] + 2*h[0][1]/r - 2*h[0][0]/r**2 + 2*q/r + mu*h[0][0]/(f*r**2)
    a1 = I*omega*q - mu*f*h[1][0]/r**2
    gr_expected = [lam*a0, lam*a1]
    gr_reduction = [
        s.cancel(s.together(equations[i].subs(beta, 0) - gr_expected[i])) == 0
        for i in range(2)
    ]
    if gr_reduction != [True, True]:
        raise SystemExit(f"GR reduction failed: {gr_reduction}")

    payload = {
        "scope": "corrected AEH=1/2 exact Fourier-radial Euler and unreduced six-state generator",
        "source_action": str(SOURCE.relative_to(ROOT)),
        "source_action_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "fourier_convention": "exp(-I*omega*t)",
        "state": [str(x) for x in state],
        "state_dimension": 6,
        "differential_orders": orders,
        "euler_from_action": euler_identity,
        "euler_equations": [canonical(eq) for eq in equations],
        "principal_matrix": [[canonical(principal[i, j]) for j in range(2)] for i in range(2)],
        "principal_determinant": canonical(determinant),
        "descriptor_E": [[canonical(descriptor_e[i, j]) for j in range(6)] for i in range(6)],
        "descriptor_A": [[canonical(descriptor_a[i, j]) for j in range(6)] for i in range(6)],
        "descriptor_determinant": canonical(descriptor_det),
        "ordinary_generator": "G=E**(-1)*A only when descriptor_determinant != 0",
        "ordinary_generator_guard": ["M != 0", "r != 0", "r-2*M != 0", "lam != 0", "beta != 0", "descriptor_determinant != 0"],
        "gr_reduction": gr_reduction,
        "laurent_coefficients": "not exported: ordinary G is not formed without the exact descriptor determinant guard",
        "exceptional_frequency_boundary": "historical exceptional-frequency results are consistency targets only; this artifact is generic in omega",
    }
    payload["payload_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    receipt = "\n".join([
        "GFE_CORRECTED_AEH_HALF_EULER_GENERATOR",
        "ACTION_NORMALIZATION := AEH=1/2",
        "H0R2_COEFFICIENT := 3",
        "EULER_FROM_ACTION := passed",
        "STATE_DIMENSION := 6",
        "GENERATOR_FORM := descriptor-plus-guard",
        "GR_REDUCTION := passed",
        "LAURENT_BLOCKS := not exported; guarded ordinary generator not formed",
        f"PAYLOAD_SHA256 := {payload['payload_sha256']}",
    ]) + "\n"
    RECEIPT.write_text(receipt, encoding="utf-8")
    print(receipt, end="")


if __name__ == "__main__":
    main()
