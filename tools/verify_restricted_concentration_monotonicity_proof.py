#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/restricted_concentration_monotonicity_proof_2026_05_23.json"
doc = ROOT / "docs/status/RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedConcentrationMonotonicityProof.lean"

data = json.loads(artifact.read_text())

assert data["name"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF"
assert data["status"] == "PROOF_SURFACE_ONLY_RESTRICTED_CONCENTRATION_MONOTONICITY_NOT_UNCONDITIONAL"
assert data["previous_object"] == "LOCAL_BALANCE_LAW_DQDT_DERIVATION"
assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"

for token in [
    "LOCAL_BALANCE_LAW_DQDT_DERIVATION",
    "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE",
]:
    assert token in data["uses"]

for token in [
    "localBalanceLawDQDTDerived",
    "stressEnergyConserved",
    "weakEnergyCondition",
    "dominantEnergyCondition",
    "bootstrapInequalitiesB",
    "fluxDominance",
    "deformationErrorControlled",
    "nonsymmetricErrorControlled",
    "etaRange",
    "fluxDominanceAbsorbsErrors",
    "qDerivativeNonnegative",
    "nonnegativeDerivativeImpliesConcentrationMonotone",
]:
    assert token in data["assumptions"]

for boundary in [
    "proof surface only",
    "local balance-law dQ/dt derivation remains conditional",
    "flux-dominance absorption step assumed",
    "qDerivativeNonnegative extraction assumed",
    "monotonicity-from-derivative step assumed",
    "no unconditional restricted concentration monotonicity theorem",
    "no restricted continuation norm control proof",
    "no package compatibility proof",
    "no target-interface compatibility proof",
    "no concrete analytic Einstein-matter estimate package proof",
    "no gravity closure",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]:
    assert boundary in data["boundary"]

doc_text = doc.read_text()
for token in [
    "PROOF_SURFACE_ONLY_RESTRICTED_CONCENTRATION_MONOTONICITY_NOT_UNCONDITIONAL",
    "LOCAL_BALANCE_LAW_DQDT_DERIVATION",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
]:
    assert token in doc_text

lean_text = lean.read_text()
for token in [
    "RestrictedConcentrationMonotonicityProofData",
    "RestrictedConcentrationMonotonicityProofHypotheses",
    "LocalBalanceLawDQDTDerivationData",
    "RestrictedLocalConcentrationData",
    "RestrictedLocalFluxTerms",
    "fluxDominanceAbsorbsErrors",
    "qDerivativeNonnegative",
    "nonnegativeDerivativeImpliesConcentrationMonotone",
    "RestrictedConcentrationMonotonicityProof",
]:
    assert token in lean_text

print("Restricted concentration monotonicity proof verifier OK.")
print("Status:", data["status"])
print("Next admissible object:", data["next_admissible_object"])
