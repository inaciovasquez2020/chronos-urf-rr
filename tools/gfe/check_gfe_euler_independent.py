#!/usr/bin/env python3
"""Independent Euler-Lagrange cross-check for the corrected AEH=1/2 action.

This checker does not import or call derive_gfe_corrected_euler_generator.py.
It computes the multi-index Euler operator directly, using a separate total
derivative implementation, applies the Fourier convention, and compares the
result with the exported equations.
"""
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_full_lagrangian.json"
EXPORTED = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"

M, r, beta, lam, omega = s.symbols("M r beta lam omega")
I = s.I
jets = {
    (field, to, ro): s.Symbol(f"h{field}t{to}r{ro}")
    for field in range(2) for to in range(5) for ro in range(5)
}
locals_map = {"M": M, "r": r, "beta": beta, "lam": lam,
              "lambda": lam, "omega": omega, "I": I}
locals_map.update({str(jet): jet for jet in jets.values()})


def total_derivative(expr, direction):
    """Apply D_t or D_r on the finite jet algebra without the producer helper."""
    out = s.diff(expr, r) if direction == "r" else s.Integer(0)
    dt, dr = (1, 0) if direction == "t" else (0, 1)
    for (field, to, ro), jet in jets.items():
        next_jet = jets.get((field, to + dt, ro + dr))
        if next_jet is not None:
            partial = s.diff(expr, jet)
            if partial != 0:
                out += partial * next_jet
    return s.expand(out)


def euler_operator(lagrangian, field):
    result = s.Integer(0)
    for (jet_field, to, ro), jet in jets.items():
        if jet_field != field:
            continue
        partial = s.diff(lagrangian, jet)
        if partial == 0:
            continue
        for _ in range(to):
            partial = total_derivative(partial, "t")
        for _ in range(ro):
            partial = total_derivative(partial, "r")
        result += (-1) ** (to + ro) * partial
    return s.expand(result)


def radial_fourier(expr):
    replacements = {
        jet: (-I * omega) ** to * s.Symbol(f"h{field}r{ro}")
        for (field, to, ro), jet in jets.items()
    }
    return s.expand(expr.xreplace(replacements))


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    exported = json.loads(EXPORTED.read_text(encoding="utf-8"))
    lagrangian = s.sympify(
        source["full_lagrangian"].replace("lambda", "lam"),
        locals=locals_map,
    )
    expected = [
        s.sympify(eq, locals={**locals_map, **{
            f"h{field}r{order}": s.Symbol(f"h{field}r{order}")
            for field in range(2) for order in range(5)
        }})
        for eq in exported["euler_equations"]
    ]
    actual = [radial_fourier(euler_operator(lagrangian, field))
              for field in range(2)]
    for field, (lhs, rhs) in enumerate(zip(actual, expected)):
        difference = s.cancel(s.together(lhs - rhs))
        if difference != 0:
            raise SystemExit(f"independent Euler-Lagrange mismatch for field {field}")
        print(f"independent Euler-Lagrange field {field}: PASS", flush=True)
    print("PASS: source action independently reproduces both exported Fourier-radial Euler equations.")


if __name__ == "__main__":
    main()
