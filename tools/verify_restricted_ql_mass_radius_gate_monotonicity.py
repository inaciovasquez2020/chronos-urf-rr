#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ART = Path("artifacts/chronos/restricted_ql_mass_radius_gate_monotonicity_2026_05_28.json")
DOC = Path("docs/status/RESTRICTED_QL_MASS_RADIUS_GATE_MONOTONICITY_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/RestrictedQLMassRadiusGateMonotonicity.lean")
ROOT = Path("lean/Chronos.lean")

required = [ART, DOC, LEAN, ROOT]
missing = [str(p) for p in required if not p.exists()]

if missing:
    print("MISSING:", missing)
    sys.exit(1)

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()

assert data["status"] == "SOLVED_RESTRICTED_LOCAL_ARITHMETIC_GATE_ONLY"
assert "restrictedQLCollapseGate_mono_massRadius" in lean
assert "restrictedQLCollapseGate_zero_mass_rigid" in lean
assert "Nat.le_trans" in lean
assert "Nat.eq_zero_of_le_zero" in lean
assert "import Chronos.Frontier.RestrictedQLMassRadiusGateMonotonicity" in root

for token in [
    "cosmic censorship proved",
    "hoop conjecture proved",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted Chronos-RR proved",
    "unrestricted H4.1/FGL proved",
    "solves P vs NP",
    "Clay problem solved",
]:
    assert token in data["does_not_prove"]
    assert token in doc

print("RESTRICTED_QL_MASS_RADIUS_GATE_MONOTONICITY_OK")
