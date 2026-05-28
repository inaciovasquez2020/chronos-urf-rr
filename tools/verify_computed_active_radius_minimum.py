#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ART = Path("artifacts/chronos/computed_active_radius_minimum_2026_05_28.json")
DOC = Path("docs/status/COMPUTED_ACTIVE_RADIUS_MINIMUM_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/ComputedActiveRadiusMinimum.lean")
ROOT = Path("lean/Chronos.lean")

missing = [str(p) for p in [ART, DOC, LEAN, ROOT] if not p.exists()]
if missing:
    print("MISSING:", missing)
    sys.exit(1)

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()

assert data["status"] == "SOLVED_RESTRICTED_COMPUTED_ACTIVE_RADIUS_MINIMUM_ONLY"
assert "import Chronos.Frontier.RestrictedQLFiniteDetectorMassRadiusExtraction" in lean
assert "def activeDetectors" in lean
assert "def activeRadiusValues" in lean
assert "def computedActiveRadiusMinimum" in lean
assert "Finset.min'" in lean
assert "theorem active_radius_mem_values_of_active" in lean
assert "theorem computedActiveRadiusMinimum_le_active_radius" in lean
assert "theorem finiteDetectorExtraction_gate_of_computed_min_le_mass" in lean
assert "theorem finiteDetectorExtraction_computed_min_gate_mono_mass" in lean
assert "import Chronos.Frontier.ComputedActiveRadiusMinimum" in root

for banned in ["sorry", "admit", "axiom"]:
    assert banned not in lean

for token in [
    "cosmic censorship proved",
    "hoop conjecture proved",
    "Einstein-matter PDE well-posedness",
    "trapped-surface formation theorem",
    "black-hole formation theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted Chronos-RR proved",
    "unrestricted H4.1/FGL proved",
    "solves P vs NP",
    "Clay problem solved"
]:
    assert token in data["does_not_prove"]
    assert token in doc

print("COMPUTED_ACTIVE_RADIUS_MINIMUM_OK")
