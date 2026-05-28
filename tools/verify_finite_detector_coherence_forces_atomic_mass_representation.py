#!/usr/bin/env python3
import json
from pathlib import Path

lean = Path("lean/Chronos/Frontier/FiniteDetectorCoherenceForcesAtomicMassRepresentation.lean")
artifact = Path("artifacts/chronos/finite_detector_coherence_forces_atomic_mass_representation_2026_05_28.json")
doc = Path("docs/status/FINITE_DETECTOR_COHERENCE_FORCES_ATOMIC_MASS_REPRESENTATION_2026_05_28.md")

required_lean = [
    "structure FiniteDetectorCoherentExtraction",
    "finiteDetectorCoherence_forces_atomicMassRepresentation",
    "finiteDetectorCoherence_uniqueExtraction",
    "finiteDetectorCoherence_noRegroupingObstruction",
    "C.extract A = A.sum C.atomMass",
]

required_doc = [
    "FINITE_COHERENCE_THEOREM_SOLVED",
    "not a replacement for that infrastructure",
    "forced invariant",
    "finite regrouping dependence",
    "does not prove",
    "P vs NP",
    "any Clay problem",
]

for path in [lean, artifact, doc]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in required_doc:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

if data.get("status") != "FINITE_COHERENCE_THEOREM_SOLVED":
    raise SystemExit("bad artifact status")

for theorem in [
    "finiteDetectorCoherence_forces_atomicMassRepresentation",
    "finiteDetectorCoherence_uniqueExtraction",
    "finiteDetectorCoherence_noRegroupingObstruction",
]:
    if theorem not in data.get("closed_theorems", []):
        raise SystemExit(f"missing closed theorem: {theorem}")

for forbidden_boundary in [
    "physical detector-field extraction map",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if forbidden_boundary not in data.get("does_not_prove", []):
        raise SystemExit(f"missing boundary: {forbidden_boundary}")

print("FINITE_DETECTOR_COHERENCE_FORCES_ATOMIC_MASS_REPRESENTATION_OK")
