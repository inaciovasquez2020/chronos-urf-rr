#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "lean/Chronos/Frontier/UniversalBoundaryCompactnessConditionalBridge.lean"
doc = root / "docs/status/UNIVERSAL_BOUNDARY_COMPACTNESS_CONDITIONAL_BRIDGE_2026_05_16.md"
artifact = root / "artifacts/chronos/universal_boundary_compactness_conditional_bridge_2026_05_16.json"
imports = root / "lean/Chronos.lean"

for path in [lean, doc, artifact, imports]:
    assert path.exists(), f"missing {path}"

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()
import_text = imports.read_text()
data = json.loads(artifact_text)

required_lean = [
    "structure FiniteEnergyMatterAdmissibilityWitness",
    "def FiniteEnergyMatterAdmissibility",
    "structure BackreactionControlWitness",
    "def BackreactionControlTheorem",
    "structure CovariantEntropyBoundInput",
    "def CovariantEntropyBoundAvailable",
    "structure UniversalBoundaryCompactnessConditionalConclusion",
    "theorem universalBoundaryCompactness_conditional_bridge",
    "structure UniversalBoundaryCompactnessConditionalBridgeStatus",
    "def conditionalBridgeStatus",
    "cosmicCensorshipPromotionBlocked",
    "hoopConjecturePromotionBlocked",
]

for token in required_lean:
    assert token in lean_text, token

required_doc = [
    "Status: CONDITIONAL_BRIDGE_ONLY",
    "FiniteEnergyMatterAdmissibility as FRONTIER_OPEN input.",
    "BackreactionControlTheorem as FRONTIER_OPEN input.",
    "CovariantEntropyBoundInput as EXTERNAL_INPUT.",
    "Conditional bridge only.",
    "Does not prove:",
    "Cosmic Censorship",
    "the Hoop Conjecture",
]

for token in required_doc:
    assert token in doc_text, token

assert data["status"] == "CONDITIONAL_BRIDGE_ONLY"
assert data["theorem_promotion"] is False
assert "FiniteEnergyMatterAdmissibility" in data["frontier_open_inputs"]
assert "BackreactionControlTheorem" in data["frontier_open_inputs"]
assert "CovariantEntropyBoundInput" in data["external_inputs"]
assert "Cosmic Censorship" in data["forbidden_overclaim_guards"]
assert "Hoop Conjecture" in data["forbidden_overclaim_guards"]
assert "import Chronos.Frontier.UniversalBoundaryCompactnessConditionalBridge" in import_text

combined = "\n".join([lean_text, doc_text, artifact_text]).lower()

forbidden = [
    "proves finiteenergymatteradmissibility",
    "proves finite-energy matter admissibility",
    "proves backreactioncontroltheorem",
    "proves backreaction control",
    "proves covariantentropyboundinput",
    "proves covariant entropy bound",
    "proves einsteindynamicsregularitytransfer",
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

print("Universal boundary compactness conditional bridge verified.")
