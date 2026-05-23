#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean_file = ROOT / "lean/Chronos/Frontier/GenuineAnalyticEstimatePackageProofReduction.lean"
artifact_file = ROOT / "artifacts/chronos/genuine_analytic_estimate_package_proof_reduction_2026_05_22.json"
doc_file = ROOT / "docs/status/GENUINE_ANALYTIC_ESTIMATE_PACKAGE_PROOF_REDUCTION_2026_05_22.md"
chronos_file = ROOT / "lean/Chronos.lean"

lean = lean_file.read_text()
artifact = json.loads(artifact_file.read_text())
doc = doc_file.read_text()
chronos = chronos_file.read_text()

assert "import Chronos.Frontier.GenuineAnalyticEstimatePackageProofReduction" in chronos
assert "import Chronos.Frontier.AnalyticEstimatePackageExistsProof" in lean
assert "structure GenuineEinsteinMatterDatum" in lean
assert "structure GenuinePDEEstimateWitness" in lean
assert "def analyticEstimatePackage_from_genuinePDEEstimateWitness" in lean
assert "theorem analyticEstimatePackageExists_from_genuinePDEEstimateWitness" in lean
assert "theorem bootstrapKernel_from_genuinePDEEstimateWitness" in lean
assert "theorem collapseGate_from_genuinePDEEstimateWitness" in lean
assert "def GenuineAnalyticEstimatePackageExistsProof : Prop" in lean
assert "theorem analyticEstimatePackageExists_from_genuineProof" in lean
assert "axiom " not in lean

assert artifact["status"] == "GENUINE_PDE_WITNESS_REDUCTION_CLOSED_GENUINE_PDE_WITNESS_OPEN"
assert artifact["next_admissible_object"] == "GENUINE_PDE_ESTIMATE_WITNESS"

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

print("Genuine analytic estimate package proof reduction verification OK.")
print(f"Status: {artifact['status']}")
print(f"Next admissible object: {artifact['next_admissible_object']}")
