#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "lean/Chronos/Frontier/AdmissibilityGatedBridgeIngredientKernel.lean"
artifact = ROOT / "artifacts/chronos/admissibility_gated_bridge_ingredient_kernel_2026_05_24.json"
status = ROOT / "docs/status/ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_KERNEL_2026_05_24.md"

lean_text = lean.read_text()
status_text = status.read_text()
data = json.loads(artifact.read_text())

for token in [
    "structure AdmissibilityGate",
    "structure BridgeIngredientKernel",
    "def R2DiameterFillingCompatibilityGate",
    "def R3UniformLocalTypeCapacityGate",
    "def NonFactorisationAdmissibleBridgeGate",
    "def R2AdmissibilityGatedBridgeIngredient",
    "def R3AdmissibilityGatedBridgeIngredient",
    "def NonFactorisationAdmissibilityGatedBridgeIngredient",
    "theorem r2_gate_excludes_refuted_naive_route_class",
    "theorem r2_gate_supplies_positive_invariant",
    "theorem r3_gate_excludes_refuted_naive_route_class",
    "theorem r3_gate_supplies_positive_invariant",
    "theorem non_factorisation_gate_excludes_refuted_naive_route_class",
    "theorem non_factorisation_gate_supplies_positive_invariant",
    "theorem admissibility_gated_bridge_ingredient_count",
    "theorem no_theorem_target_closed_by_admissibility_gated_kernel",
]:
    assert token in lean_text, token

assert data["status"] == "ADMISSIBILITY_GATED_BRIDGE_INGREDIENT_KERNEL_ADDED_THEOREM_TARGETS_OPEN"
assert data["new_bridge_ingredient"] == "AdmissibilityGatedBridgeIngredientKernel"
assert data["ingredient_count"] == 3
assert data["theorem_target_closure_count"] == 0
assert len(data["ingredients"]) == 3
assert len(data["gates"]) == 3
assert len(data["closed_kernel_facts"]) == 6

for token in [
    "DiameterSeparationFillingObstructionProofTarget",
    "UniformLocalTypeCapacityProofTarget",
    "NonFactorisationBridgeProofTarget",
    "FourBridgesSourceSolved theorem closure",
    "R2 theorem target closure",
    "R3 theorem target closure",
    "NON_FACTORISATION theorem target closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in status_text, token
    assert token in data["still_open"] or token in data["does_not_prove"], token

print("admissibility gated bridge ingredient kernel verifier OK")
