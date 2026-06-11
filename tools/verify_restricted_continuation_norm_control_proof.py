#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_proof_2026_06_11.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF_2026_06_11.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControlProof.lean"

data = json.loads(artifact.read_text())
doc_text = doc.read_text()
lean_text = lean.read_text()

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"
assert data["status"] == "PROOF_OBLIGATION_SURFACE_ONLY_NO_CONTINUATION_NORM_CONTROL_PROOF"
assert data["previous_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF"
assert data["next_admissible_object"] == "PACKAGE_COMPATIBILITY_PROOF"

expected_obligations = [
    "restrictedConcentrationMonotonicityAvailable",
    "continuationNormDefined",
    "continuationIntervalControlled",
    "bootstrapNormBoundPropagates",
    "concentrationControlsContinuationNorm",
    "thresholdNotReached",
    "continuationCriterionApplies",
]
assert data["obligations"] == expected_obligations

expected_boundary = [
    "proof-obligation surface only",
    "no unconditional restricted continuation norm control theorem",
    "no package compatibility proof",
    "no target-interface compatibility proof",
    "no concrete analytic Einstein-matter estimate package proof",
    "no gravity closure",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]
assert data["boundary"] == expected_boundary

required_tokens = [
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "PROOF_OBLIGATION_SURFACE_ONLY_NO_CONTINUATION_NORM_CONTROL_PROOF",
    "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF",
    "PACKAGE_COMPATIBILITY_PROOF",
    "RestrictedContinuationNormControlProofSurfaceData",
    "RestrictedContinuationNormControlProofSurfaceObligations",
    "RestrictedContinuationNormControlProofSurface",
    "RestrictedContinuationNormControlProofSurfaceStatus",
    "RestrictedContinuationNormControlProofSurfacePreviousObject",
    "RestrictedContinuationNormControlProofSurfaceNextAdmissibleObject",
]
for token in required_tokens:
    assert token in doc_text or token in lean_text or token in json.dumps(data)

print("Restricted continuation norm-control proof-obligation verifier OK.")
print("Status: PROOF_OBLIGATION_SURFACE_ONLY_NO_CONTINUATION_NORM_CONTROL_PROOF")
print("Next admissible object: PACKAGE_COMPATIBILITY_PROOF")
