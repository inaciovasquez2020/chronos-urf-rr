#!/usr/bin/env python3
"""Independent consistency replay for the published action table.

This checks the 81 printed monomials in the report and reconstructs the
second-jet Hessian from the printed action. It does NOT recompute curvature
from the metric, so it is not a clean metric-to-action derivation replay.
"""
from pathlib import Path
import re
import sympy as sp

REPORT = Path(__file__).resolve().parents[1] / "docs/status/even_parity_cubic_quadratic_action_independent_derivation_2026-10-21.md"
text = REPORT.read_text()
section = text.index("## Exact angularly integrated coefficient")
start = text.index("```text\n", section) + len("```text\n")
end = text.index("\n```", start)
lines = text[start:end].splitlines()
M, r = sp.symbols("M r", nonzero=True)
jets = {}
terms = []
for n, line in enumerate(lines, 1):
    match = re.match(r"^\((.*)\)\*\((.*)\)(?: \+)?$", line)
    if not match:
        raise AssertionError(f"could not parse action term {n}: {line}")
    coefficient_text, monomial_text = match.groups()
    coefficient = sp.sympify(coefficient_text, locals={"M": M, "r": r})
    monomial = sp.Integer(1)
    factors = re.findall(r"([A-Za-z][A-Za-z0-9_]*)(?:\*\*(\d+))?", monomial_text)
    for name, power in factors:
        symbol = jets.setdefault(name, sp.Symbol(name))
        monomial *= symbol ** (int(power) if power else 1)
    terms.append(coefficient * monomial)
action = sp.expand(sum(terms))
assert len(lines) == 81
assert sp.Poly(action, *jets.values()).total_degree() == 2

checks = {}
checks["H2_tt_squared"] = sp.factor(
    action.coeff(jets["H2_t_t"] ** 2) - 3*M*r/(2*(r-2*M)**2)
) == 0
checks["K_tt_squared"] = sp.factor(
    action.coeff(jets["K_t_t"] ** 2) + 3*M*r/(2*(r-2*M)**2)
) == 0
checks["H0_rr_squared"] = sp.factor(
    action.coeff(jets["H0_r_r"] ** 2) - 3*M*(r-2*M)**2/(2*r**3)
) == 0

order = ["H0_r_r", "H1_t_r", "H2_t_t", "K_t_t", "K_t_r", "K_r_r"]
hessian = sp.Matrix([
    [sp.diff(action, jets[a], jets[b]) for b in order]
    for a in order
]).applyfunc(sp.factor)
top = hessian[:3, :3]
checks["top_block_determinant_zero"] = sp.factor(top.det()) == 0
checks["top_block_all_2x2_minors_zero"] = all(
    sp.factor(top.extract([i, j], [k, ell]).det()) == 0
    for i in range(3) for j in range(i+1, 3)
    for k in range(3) for ell in range(k+1, 3)
)
checks["numeric_rank_M2_r5_is_4"] = hessian.subs({M: 2, r: 5}).rank() == 4
if not all(checks.values()):
    raise SystemExit("FAIL: " + repr(checks))
print("ACTION_TABLE_PARSE: PASS (81 terms)")
for name, result in checks.items():
    print(f"{name}: {'PASS' if result else 'FAIL'}")
print("SCOPE: artifact consistency only; metric-to-curvature clean replay NOT performed")