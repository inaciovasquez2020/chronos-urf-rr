#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "lean/Chronos/Frontier/ExtractPhysicalDetectorWitness.lean"
artifact = root / "artifacts/chronos/extract_physical_detector_witness_2026_05_28.json"
doc = root / "docs/status/EXTRACT_PHYSICAL_DETECTOR_WITNESS_2026_05_28.md"
chronos = root / "lean/Chronos.lean"

for path in [lean, artifact, doc, chronos]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
required_lean = [
    "import Chronos.Frontier.FiniteDetectorPartition",
    "structure ExtractedPhysicalDetectorWitness",
    "def extractPhysicalDetectorWitness",
    "theorem extractPhysicalDetectorWitness_activeMass_eq_totalEnergy",
    "theorem extractPhysicalDetectorWitness_sampleCount_eq_supportSize",
    "theorem extractPhysicalDetectorWitness_detectorCellCount_eq_partitionCellCount",
    "theorem extractPhysicalDetectorWitness_activeDetectorIds_eq_partitionIds",
    "theorem extractPhysicalDetectorWitness_activeMass_nonnegative",
    "theorem extractPhysicalDetectorWitness_activeDetectorIds_finite",
    "theorem extractPhysicalDetectorWitness_activeDetectorIds_length_eq_detectorCellCount",
    "theorem extractPhysicalDetectorWitness_emptyData_activeMass_zero",
]
for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["axiom", "admit", "sorry"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.ExtractPhysicalDetectorWitness" not in chronos.read_text():
    raise SystemExit("Chronos.lean missing ExtractPhysicalDetectorWitness import")

data = json.loads(artifact.read_text())
if data.get("status") != "FINITE_EXTRACTION_WITNESS_OBJECT_ONLY":
    raise SystemExit("wrong artifact status")

artifact_text = artifact.read_text()
for dep in [
    "PHYSICAL_FIELD_DATA_FINITE_SAMPLES_2026_05_28",
    "FINITE_DETECTOR_PARTITION_2026_05_28",
]:
    if dep not in artifact_text:
        raise SystemExit(f"missing dependency: {dep}")

required_boundaries = [
    "PhysicalDetectorFieldExtractionMap",
    "DetectorBudgetCompatible",
    "DetectorBudgetCompatible to RestrictedFiniteDetectorExtractionGate",
    "coverage of physical field data",
    "disjointness of detector cells",
    "geometric partition correctness",
    "empirical detector correctness",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]
doc_text = doc.read_text()
for token in required_boundaries:
    if token not in doc_text:
        raise SystemExit(f"missing doc boundary: {token}")
    if token not in artifact_text:
        raise SystemExit(f"missing artifact boundary: {token}")

print("EXTRACT_PHYSICAL_DETECTOR_WITNESS_OK")
