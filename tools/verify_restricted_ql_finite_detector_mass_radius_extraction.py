#!/usr/bin/env python3
from pathlib import Path
import json, sys
ART = Path("artifacts/chronos/restricted_ql_finite_detector_mass_radius_extraction_2026_05_28.json")
DOC = Path("docs/status/RESTRICTED_QL_FINITE_DETECTOR_MASS_RADIUS_EXTRACTION_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/RestrictedQLFiniteDetectorMassRadiusExtraction.lean")
ROOT = Path("lean/Chronos.lean")
missing = [str(p) for p in [ART, DOC, LEAN, ROOT] if not p.exists()]
if missing: sys.exit("MISSING: " + repr(missing))
data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()
root = ROOT.read_text()
assert data["status"] == "SOLVED_RESTRICTED_FINITE_DETECTOR_EXTRACTION_BRIDGE_ONLY"
for s in [
    "import Chronos.Frontier.RestrictedQLMassRadiusGateMonotonicity",
    "namespace Chronos",
    "namespace Frontier",
    "def activeMass",
    "def finiteDetectorMassRadiusExtraction",
    "theorem finiteDetectorExtraction_gate_of_active_floor_le_mass",
    "theorem finiteDetectorExtraction_activeMass_mono",
    "theorem finiteDetectorExtraction_gate_mono_mass",
    "Finset.sum_le_sum",
    "Nat.le_trans"
]: assert s in lean
assert "import Chronos.Frontier.RestrictedQLFiniteDetectorMassRadiusExtraction" in root
for banned in ["sorry", "admit", "axiom"]: assert banned not in lean
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
print("RESTRICTED_QL_FINITE_DETECTOR_MASS_RADIUS_EXTRACTION_OK")
