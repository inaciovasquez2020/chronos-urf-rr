#!/usr/bin/env python3
import json
from pathlib import Path

lean = Path("lean/Chronos/Frontier/RestrictedPhysicalDetectorFieldExtractionMap.lean")
artifact = Path("artifacts/chronos/restricted_physical_detector_field_extraction_map_2026_05_28.json")
doc = Path("docs/status/RESTRICTED_PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_2026_05_28.md")

for path in [lean, artifact, doc]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure PhysicalDetectorField",
    "def activeDetectors",
    "def physicalAtomMass",
    "def extractedRadiusFloor",
    "def extractedActiveMass",
    "structure PhysicalDetectorFieldAdmissible",
    "gate_bound",
    "physicalExtraction_activeSet_correct",
    "physicalExtraction_atomMass_coherent",
    "physicalExtraction_feeds_restrictedFiniteDetectorGate",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

if data.get("status") != "CONDITIONAL_RESTRICTED_INTERFACE_BRIDGE_SOLVED":
    raise SystemExit("bad artifact status")

if "PhysicalDetectorFieldAdmissible.gate_bound" not in data.get("conditional_on", []):
    raise SystemExit("missing conditional gate_bound")

for theorem in [
    "physicalExtraction_activeSet_correct",
    "physicalExtraction_atomMass_coherent",
    "physicalExtraction_data_activeMass",
    "physicalExtraction_data_radiusFloor",
    "physicalExtraction_feeds_restrictedFiniteDetectorGate",
]:
    if theorem not in data.get("closed_theorems", []):
        raise SystemExit(f"missing closed theorem: {theorem}")

for boundary in [
    "derivation of gate_bound from raw physical readings",
    "arbitrary physical detector fields are admissible",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if boundary not in data.get("does_not_prove", []):
        raise SystemExit(f"missing boundary: {boundary}")

required_doc = [
    "CONDITIONAL_RESTRICTED_INTERFACE_BRIDGE_SOLVED",
    "Corrected Boundary Admissibility",
    "does not imply",
    "false local-to-global aggregation route",
    "does not prove",
]

for token in required_doc:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

print("RESTRICTED_PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_OK")
