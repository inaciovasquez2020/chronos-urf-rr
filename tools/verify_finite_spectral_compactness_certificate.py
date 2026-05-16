#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "lean/Chronos/Frontier/FiniteSpectralCompactnessCertificate.lean"
doc = root / "docs/status/FINITE_SPECTRAL_COMPACTNESS_CERTIFICATE_2026_05_16.md"
artifact = root / "artifacts/chronos/finite_spectral_compactness_certificate_2026_05_16.json"
imports = root / "lean/Chronos.lean"

for path in [lean, doc, artifact, imports]:
    assert path.exists(), f"missing {path}"

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()
import_text = imports.read_text()
data = json.loads(artifact_text)

required_lean = [
    "structure FiniteDetectorAlgebra",
    "structure SpectralCutoff",
    "structure BoundaryObservableStateSpace",
    "theorem boundaryObservableStateSpace_finite_dimensional",
    "structure FiniteSpectralCompactnessCertificate",
    "def constructFiniteSpectralCompactnessCertificate",
    "structure PhysicalToTopologicalCompactnessCertificate",
    "def finiteSpectralCompactness_to_physicalTopologicalCompactness",
    "def finite_detector_spectral_cutoff_constructs_physical_to_topological_compactness",
]

for token in required_lean:
    assert token in lean_text, token

assert "import Chronos.Frontier.FiniteSpectralCompactnessCertificate" in import_text
assert data["status"] == "FINITE_SPECTRAL_COMPACTNESS_CERTIFICATE_SURFACE"
assert data["theorem_promotion"] is False

required_doc = [
    "Status: FINITE_SPECTRAL_COMPACTNESS_CERTIFICATE_SURFACE",
    "Certificate construction surface only.",
    "Does not prove:",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted QL_CollapseGate",
    "Cosmic Censorship",
    "the Hoop Conjecture",
]

for token in required_doc:
    assert token in doc_text, token

combined = "\n".join([lean_text, doc_text, artifact_text]).lower()
forbidden = [
    "proves einstein dynamics",
    "proves finite-energy matter admissibility",
    "proves backreaction control",
    "proves covariant entropy bound",
    "proves unrestricted universalboundarycompactness",
    "proves unrestricted ql_collapsegate",
    "proves cosmic censorship",
    "proves the hoop conjecture",
    "proves unrestricted chronos-rr",
    "proves h4.1/fgl",
    "proves p vs np",
    "solves p vs np",
    "solves a clay problem",
    "unrestricted universalboundarycompactness is closed",
    "unrestricted ql_collapsegate is closed",
]

for token in forbidden:
    assert token not in combined, token

print("Finite spectral compactness certificate verified.")
