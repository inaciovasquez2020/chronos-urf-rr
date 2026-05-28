#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "lean/Chronos/Frontier/PhysicalFieldDataFiniteSamples.lean"
artifact = root / "artifacts/chronos/physical_field_data_finite_samples_2026_05_28.json"
doc = root / "docs/status/PHYSICAL_FIELD_DATA_FINITE_SAMPLES_2026_05_28.md"

for path in [lean, artifact, doc]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
required_lean = [
    "structure PhysicalEnergySample",
    "structure PhysicalFieldData",
    "def PhysicalFieldData.supportSize",
    "def PhysicalFieldData.totalEnergy",
    "theorem physicalFieldData_support_finite",
    "theorem physicalFieldData_totalEnergy_nonnegative",
    "theorem physicalFieldData_empty_totalEnergy_zero",
]
for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data.get("status") != "FINITE_FIELD_DATA_OBJECT_ONLY":
    raise SystemExit("wrong artifact status")

required_boundaries = [
    "PhysicalDetectorFieldExtractionMap",
    "FiniteDetectorPartition",
    "extractPhysicalDetectorWitness",
    "DetectorBudgetCompatible",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]
doc_text = doc.read_text()
artifact_text = artifact.read_text()
for token in required_boundaries:
    if token not in doc_text:
        raise SystemExit(f"missing doc boundary: {token}")
    if token not in artifact_text:
        raise SystemExit(f"missing artifact boundary: {token}")

print("PHYSICAL_FIELD_DATA_FINITE_SAMPLES_OK")
