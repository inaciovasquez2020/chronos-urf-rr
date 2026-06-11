#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/target_interface_compatibility_proof_2026_06_11.json"
doc = ROOT / "docs/status/TARGET_INTERFACE_COMPATIBILITY_PROOF_2026_06_11.md"
lean = ROOT / "lean/Chronos/Frontier/TargetInterfaceCompatibilityProof.lean"

data = json.loads(artifact.read_text())
doc_text = doc.read_text()
lean_text = lean.read_text()

assert data["name"] == "TARGET_INTERFACE_COMPATIBILITY_PROOF"
assert data["status"] == "PROOF_OBLIGATION_SURFACE_ONLY_NO_TARGET_INTERFACE_COMPATIBILITY_PROOF"
assert data["previous_object"] == "PACKAGE_COMPATIBILITY_PROOF"
assert data["next_admissible_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF"

expected_obligations = [
    "packageCompatibilityAvailable",
    "targetInterfaceDefined",
    "packageOutputInterfaceDefined",
    "packageOutputMatchesTargetInput",
    "einsteinMatterTargetDefined",
    "analyticTargetStatementMatches",
    "targetConclusionCompatible",
]
assert data["obligations"] == expected_obligations

expected_boundary = [
    "proof-obligation surface only",
    "no unconditional target-interface compatibility theorem",
    "no concrete analytic Einstein-matter estimate package proof",
    "no gravity closure",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]
assert data["boundary"] == expected_boundary

required_tokens = [
    "TARGET_INTERFACE_COMPATIBILITY_PROOF",
    "PROOF_OBLIGATION_SURFACE_ONLY_NO_TARGET_INTERFACE_COMPATIBILITY_PROOF",
    "PACKAGE_COMPATIBILITY_PROOF",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF",
    "TargetInterfaceCompatibilityProofSurfaceData",
    "TargetInterfaceCompatibilityProofSurfaceObligations",
    "TargetInterfaceCompatibilityProofSurface",
    "TargetInterfaceCompatibilityProofSurfaceStatus",
    "TargetInterfaceCompatibilityProofSurfacePreviousObject",
    "TargetInterfaceCompatibilityProofSurfaceNextAdmissibleObject",
]
for token in required_tokens:
    assert token in doc_text or token in lean_text or token in json.dumps(data)

print("Target-interface compatibility proof-obligation verifier OK.")
print("Status: PROOF_OBLIGATION_SURFACE_ONLY_NO_TARGET_INTERFACE_COMPATIBILITY_PROOF")
print("Next admissible object: CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF")
