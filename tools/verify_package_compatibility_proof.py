#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/package_compatibility_proof_2026_06_11.json"
doc = ROOT / "docs/status/PACKAGE_COMPATIBILITY_PROOF_2026_06_11.md"
lean = ROOT / "lean/Chronos/Frontier/PackageCompatibilityProof.lean"

data = json.loads(artifact.read_text())
doc_text = doc.read_text()
lean_text = lean.read_text()

assert data["name"] == "PACKAGE_COMPATIBILITY_PROOF"
assert data["status"] == "PROOF_OBLIGATION_SURFACE_ONLY_NO_PACKAGE_COMPATIBILITY_PROOF"
assert data["previous_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"
assert data["next_admissible_object"] == "TARGET_INTERFACE_COMPATIBILITY_PROOF"

expected_obligations = [
    "restrictedContinuationNormControlAvailable",
    "packageInterfaceDefined",
    "continuationNormInterfaceMatches",
    "concentrationMonotonicityInterfaceMatches",
    "analyticEstimatePackageAcceptsInputs",
    "packageAssumptionsCompatible",
    "packageConclusionCompatible",
]
assert data["obligations"] == expected_obligations

expected_boundary = [
    "proof-obligation surface only",
    "no unconditional package compatibility theorem",
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
    "PACKAGE_COMPATIBILITY_PROOF",
    "PROOF_OBLIGATION_SURFACE_ONLY_NO_PACKAGE_COMPATIBILITY_PROOF",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "TARGET_INTERFACE_COMPATIBILITY_PROOF",
    "PackageCompatibilityProofSurfaceData",
    "PackageCompatibilityProofSurfaceObligations",
    "PackageCompatibilityProofSurface",
    "PackageCompatibilityProofSurfaceStatus",
    "PackageCompatibilityProofSurfacePreviousObject",
    "PackageCompatibilityProofSurfaceNextAdmissibleObject",
]
for token in required_tokens:
    assert token in doc_text or token in lean_text or token in json.dumps(data)

print("Package compatibility proof-obligation verifier OK.")
print("Status: PROOF_OBLIGATION_SURFACE_ONLY_NO_PACKAGE_COMPATIBILITY_PROOF")
print("Next admissible object: TARGET_INTERFACE_COMPATIBILITY_PROOF")
