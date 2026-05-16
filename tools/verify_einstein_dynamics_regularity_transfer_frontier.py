#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "lean/Chronos/Frontier/EinsteinDynamicsRegularityTransferFrontier.lean"
doc = root / "docs/status/EINSTEIN_DYNAMICS_REGULARITY_TRANSFER_FRONTIER_2026_05_16.md"
artifact = root / "artifacts/chronos/einstein_dynamics_regularity_transfer_frontier_2026_05_16.json"
imports = root / "lean/Chronos.lean"

for path in [lean, doc, artifact, imports]:
    assert path.exists(), f"missing {path}"

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()
import_text = imports.read_text()
data = json.loads(artifact_text)

required_lean = [
    "structure EinsteinMatterDevelopment",
    "structure EinsteinEquationSatisfied",
    "structure BoundaryFluxBound",
    "structure BackreactionControlled",
    "structure EinsteinDynamicsRegularityInput",
    "def EinsteinDynamicsRegularityTransfer",
    "structure EinsteinDynamicsRegularityTransferFrontier",
    "def regularityTransferFrontier",
    "def EinsteinDynamicsCompactnessTransferTarget",
    "structure EinsteinDynamicsCompactnessTransferStatus",
    "def compactnessTransferStatus",
]

for token in required_lean:
    assert token in lean_text, token

required_doc = [
    "Status: FRONTIER_OPEN",
    "EinsteinDynamicsRegularityTransfer:",
    "FRONTIER_OPEN weakest missing lemma only.",
    "Does not prove:",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted QL_CollapseGate",
    "Cosmic Censorship",
    "the Hoop Conjecture",
]

for token in required_doc:
    assert token in doc_text, token

assert data["status"] == "FRONTIER_OPEN"
assert data["weakest_missing_lemma"] == "EinsteinDynamicsRegularityTransfer"
assert data["theorem_promotion"] is False
assert "import Chronos.Frontier.EinsteinDynamicsRegularityTransferFrontier" in import_text

combined = "\n".join([lean_text, doc_text, artifact_text]).lower()
forbidden = [
    "proves einstein dynamics",
    "proves einsteindynamicsregularitytransfer",
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
    "cosmic censorship is closed",
    "hoop conjecture is closed",
]

for token in forbidden:
    assert token not in combined, token

print("Einstein dynamics regularity transfer frontier verified.")
