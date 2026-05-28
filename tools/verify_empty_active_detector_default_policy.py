#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ART = Path("artifacts/chronos/empty_active_detector_default_policy_2026_05_28.json")
DOC = Path("docs/status/EMPTY_ACTIVE_DETECTOR_DEFAULT_POLICY_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/EmptyActiveDetectorDefaultPolicy.lean")
ROOT = Path("lean/Chronos.lean")

missing = [str(p) for p in [ART, DOC, LEAN, ROOT] if not p.exists()]
if missing:
    print("MISSING:", missing)
    sys.exit(1)

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()

assert data["status"] == "SOLVED_RESTRICTED_EMPTY_ACTIVE_DETECTOR_DEFAULT_POLICY_ONLY"
assert "import Chronos.Frontier.ComputedActiveRadiusMinimum" in lean
assert "def defaultActiveRadiusFloor" in lean
assert "theorem defaultActiveRadiusFloor_eq_computed_of_nonempty" in lean
assert "theorem defaultActiveRadiusFloor_eq_zero_of_empty" in lean
assert "theorem activeRadiusValues_empty_of_no_active" in lean
assert "theorem activeMass_eq_zero_of_no_active" in lean
assert "theorem defaultActiveRadiusFloor_eq_zero_of_no_active" in lean
assert "theorem finiteDetectorExtraction_gate_of_default_floor_le_mass" in lean
assert "theorem finiteDetectorExtraction_no_active_default_gate" in lean
assert "import Chronos.Frontier.EmptyActiveDetectorDefaultPolicy" in root

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

print("EMPTY_ACTIVE_DETECTOR_DEFAULT_POLICY_OK")
