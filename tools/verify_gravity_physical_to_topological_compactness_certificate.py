#!/usr/bin/env python3
from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/GravityPhysicalToTopologicalCompactnessCertificate.lean")
root = Path("lean/Chronos.lean")
artifact = Path("artifacts/chronos/gravity_physical_to_topological_compactness_certificate_2026_05_16.json")
status = Path("docs/status/GRAVITY_PHYSICAL_TO_TOPOLOGICAL_COMPACTNESS_CERTIFICATE_2026_05_16.md")

for p in [lean, root, artifact, status]:
    assert p.exists(), f"missing {p}"

lean_text = lean.read_text()
root_text = root.read_text()
artifact_data = json.loads(artifact.read_text())
status_text = status.read_text()

required_lean = [
    "import Chronos.Frontier.GravityA3BoundaryCompactnessFromFiniteDetector",
    "structure FiniteSpectralCompactnessCertificate",
    "compact_space : BoundaryCompactSpace FΛ",
    "theorem physicalToTopologicalCompactnessInput_from_certificate",
    "PhysicalToTopologicalCompactnessInput FΛ Λ",
    "theorem A3BoundaryCompactnessBridge_from_certificate",
    "structure PhysicalToTopologicalCompactnessCertificateStatusLock",
    "theorem physical_to_topological_compactness_certificate_status_lock",
]

for phrase in required_lean:
    assert phrase in lean_text, phrase

assert "axiom " not in lean_text
assert "admit" not in lean_text
assert "sorry" not in lean_text

assert "import Chronos.Frontier.GravityPhysicalToTopologicalCompactnessCertificate" in root_text

assert artifact_data["status"] == "CERTIFICATE_REDUCTION_PROVED"
assert artifact_data["main_theorem"] == "physicalToTopologicalCompactnessInput_from_certificate"
assert artifact_data["remaining_missing_object"] == "FiniteSpectralCompactnessCertificate FΛ Λ"

required_status = [
    "Status: `CERTIFICATE_REDUCTION_PROVED`",
    "`PhysicalToTopologicalCompactnessInput` is proved from `FiniteSpectralCompactnessCertificate`.",
    "Remaining missing object",
    "`FiniteSpectralCompactnessCertificate FΛ Λ`",
    "Certificate reduction only.",
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
    "constructs FiniteSpectralCompactnessCertificate",
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

print("Gravity physical-to-topological compactness certificate verified: CERTIFICATE_REDUCTION_PROVED.")
