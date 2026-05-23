#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/restricted_local_concentration_monotonicity_with_flux_dominance_2026_05_23.json"
doc = ROOT / "docs/status/RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedLocalConcentrationMonotonicityWithFluxDominance.lean"

data = json.loads(artifact.read_text())

assert data["name"] == "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE"
assert data["status"] == "ESTIMATE_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE"
assert data["supplies_next_analytic_ingredient_for"] == "RESTRICTED_CONCENTRATION_MONOTONICITY"
assert "local balance law for dQ/dt" in data["assumptions"]
assert "dQ/dt >= 0; therefore concentrationMonotone" == data["conclusion"]
for field in ["flux_in", "flux_out", "deformation_error", "nonsymmetric_error"]:
    assert field in data["formalized_definitions"]

required_boundaries = [
    "no analytic Einstein-matter bootstrap package",
    "no concrete analytic Einstein-matter estimate package",
    "no finite continuation norm proof",
    "no bootstrap bound proof",
    "no threshold crossing proof",
    "no gravity closure",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]
for boundary in required_boundaries:
    assert boundary in data["boundary"]

text = doc.read_text()
assert "ESTIMATE_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE" in text
assert "RESTRICTED_CONCENTRATION_MONOTONICITY" in text
assert "RESTRICTED_CONTINUATION_NORM_CONTROL" in text

lean_text = lean.read_text()
assert "RestrictedLocalFluxTerms" in lean_text
assert "flux_in" in lean_text
assert "flux_out" in lean_text
assert "deformation_error" in lean_text
assert "nonsymmetric_error" in lean_text
assert "localBalanceLaw" in lean_text
assert "RestrictedLocalConcentrationMonotonicityWithFluxDominance" in lean_text

print("Restricted local concentration monotonicity with flux dominance verifier OK.")
print("Status:", data["status"])
print("Supplies:", data["supplies_next_analytic_ingredient_for"])
