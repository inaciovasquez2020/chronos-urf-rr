#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean_file = ROOT / "lean/Chronos/Frontier/GenuinePDEEstimateWitnessComponents.lean"
artifact_file = ROOT / "artifacts/chronos/genuine_pde_estimate_witness_components_2026_05_22.json"
doc_file = ROOT / "docs/status/GENUINE_PDE_ESTIMATE_WITNESS_COMPONENTS_2026_05_22.md"
chronos_file = ROOT / "lean/Chronos.lean"

lean = lean_file.read_text()
artifact = json.loads(artifact_file.read_text())
doc = doc_file.read_text()
chronos = chronos_file.read_text()

assert "import Chronos.Frontier.GenuinePDEEstimateWitnessComponents" in chronos
assert "import Chronos.Frontier.GenuineAnalyticEstimatePackageProofReduction" in lean
assert "structure GenuinePDEEstimateWitnessComponents" in lean
assert "constraint_propagation" in lean
assert "energy_condition_preservation" in lean
assert "continuation_up_to_collapse_threshold" in lean
assert "collapse_criterion_from_restricted_seed" in lean
assert "def genuinePDEEstimateWitness_from_components" in lean
assert "theorem analyticEstimatePackageExists_from_genuinePDEComponents" in lean
assert "theorem bootstrapKernel_from_genuinePDEComponents" in lean
assert "theorem collapseGate_from_genuinePDEComponents" in lean
assert "def GenuinePDEEstimateWitnessComponentsExist : Prop" in lean
assert "axiom " not in lean

assert artifact["status"] == "FOUR_COMPONENT_ASSEMBLY_CLOSED_PDE_COMPONENT_PROOFS_OPEN"
assert artifact["next_admissible_object"] == "GENUINE_PDE_ESTIMATE_WITNESS_COMPONENTS_EXIST"

for component in [
    "constraint_propagation",
    "energy_condition_preservation",
    "continuation_up_to_collapse_threshold",
    "collapse_criterion_from_restricted_seed",
]:
    assert component in artifact["four_components"]
    assert component in doc

for token in [
    "genuine Einstein-matter PDE existence",
    "genuine Einstein-matter PDE regularity",
    "genuine Einstein-matter PDE continuation",
    "unconditional gravity closure",
    "unrestricted gravity closure",
    "cosmic censorship",
    "hoop conjecture",
    "four-dimensional collapse theorem",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in artifact["does_not_prove"]
    assert token in doc

print("Genuine PDE estimate witness components verification OK.")
print(f"Status: {artifact['status']}")
print(f"Next admissible object: {artifact['next_admissible_object']}")
