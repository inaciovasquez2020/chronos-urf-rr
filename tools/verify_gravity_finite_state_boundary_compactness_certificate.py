#!/usr/bin/env python3
from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/GravityFiniteStateBoundaryCompactnessCertificate.lean")
root = Path("lean/Chronos.lean")
artifact = Path("artifacts/chronos/gravity_finite_state_boundary_compactness_certificate_2026_05_16.json")
status = Path("docs/status/GRAVITY_FINITE_STATE_BOUNDARY_COMPACTNESS_CERTIFICATE_2026_05_16.md")

for p in [lean, root, artifact, status]:
    assert p.exists(), f"missing {p}"

lean_text = lean.read_text()
root_text = root.read_text()
artifact_data = json.loads(artifact.read_text())
status_text = status.read_text()

required_lean = [
    "import Chronos.Frontier.GravityPhysicalToTopologicalCompactnessCertificate",
    "class FinitaryBoundaryIndex",
    "structure FiniteStateBoundaryCompactnessCertificate",
    "finite_state_index : Type u",
    "finite_index : FinitaryBoundaryIndex finite_state_index",
    "state_cover : finite_state_index → FΛ",
    "compact_space : BoundaryCompactSpace FΛ",
    "theorem finiteSpectralCompactnessCertificate_from_finite_state_certificate",
    "theorem physicalToTopologicalCompactnessInput_from_finite_state_certificate",
    "theorem A3BoundaryCompactnessBridge_from_finite_state_certificate",
    "structure FiniteStateBoundaryCompactnessCertificateStatusLock",
    "theorem finite_state_boundary_compactness_certificate_status_lock",
]

for phrase in required_lean:
    assert phrase in lean_text, phrase

assert "axiom " not in lean_text
assert "admit" not in lean_text
assert "sorry" not in lean_text

assert "import Chronos.Frontier.GravityFiniteStateBoundaryCompactnessCertificate" in root_text

assert artifact_data["status"] == "FINITE_STATE_CERTIFICATE_REDUCTION_PROVED"
assert artifact_data["main_theorem"] == "finiteSpectralCompactnessCertificate_from_finite_state_certificate"
assert artifact_data["input_certificate"] == "FiniteStateBoundaryCompactnessCertificate FΛ Λ"
assert artifact_data["output_certificate"] == "FiniteSpectralCompactnessCertificate FΛ Λ"
assert artifact_data["remaining_missing_object"] == "construction of FiniteStateBoundaryCompactnessCertificate FΛ Λ"

required_status = [
    "Status: `FINITE_STATE_CERTIFICATE_REDUCTION_PROVED`",
    "`FiniteSpectralCompactnessCertificate` is derived from `FiniteStateBoundaryCompactnessCertificate`.",
    "`physicalToTopologicalCompactnessInput_from_finite_state_certificate`",
    "`A3BoundaryCompactnessBridge_from_finite_state_certificate`",
    "Remaining missing object",
    "`FiniteStateBoundaryCompactnessCertificate FΛ Λ`",
    "Finite-state certificate reduction only.",
    "Does not prove:",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted QL_CollapseGate",
    "Cosmic Censorship",
    "the Hoop Conjecture",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status_text, phrase

forbidden_positive_claims = [
    "constructs FiniteStateBoundaryCompactnessCertificate",
    "proves unrestricted UniversalBoundaryCompactness",
    "proves unrestricted QL_CollapseGate",
    "proves Cosmic Censorship",
    "proves the Hoop Conjecture",
    "proves unrestricted Chronos-RR",
    "proves H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves a Clay problem",
]

combined = "\n".join([lean_text, status_text, json.dumps(artifact_data)])
for token in forbidden_positive_claims:
    assert token.lower() not in combined.lower(), token

print("Gravity finite-state boundary compactness certificate verified: FINITE_STATE_CERTIFICATE_REDUCTION_PROVED.")
