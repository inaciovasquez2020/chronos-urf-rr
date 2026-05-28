#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "lean/Chronos/Frontier/FiniteDetectorPartition.lean"
artifact = root / "artifacts/chronos/finite_detector_partition_2026_05_28.json"
doc = root / "docs/status/FINITE_DETECTOR_PARTITION_2026_05_28.md"
chronos = root / "lean/Chronos.lean"

for path in [lean, artifact, doc, chronos]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
required_lean = [
    "import Chronos.Frontier.PhysicalFieldDataFiniteSamples",
    "structure DetectorCell",
    "def DetectorCell.width",
    "theorem detectorCell_width_nonnegative",
    "structure FiniteDetectorPartition",
    "def FiniteDetectorPartition.cellCount",
    "def FiniteDetectorPartition.activeCellIds",
    "theorem finiteDetectorPartition_cells_finite",
    "theorem finiteDetectorPartition_empty_cellCount_zero",
    "theorem finiteDetectorPartition_activeCellIds_finite",
    "theorem finiteDetectorPartition_activeCellIds_length_eq_cellCount",
]
for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["axiom", "admit", "sorry"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.FiniteDetectorPartition" not in chronos.read_text():
    raise SystemExit("Chronos.lean missing FiniteDetectorPartition import")

data = json.loads(artifact.read_text())
if data.get("status") != "FINITE_PARTITION_OBJECT_ONLY":
    raise SystemExit("wrong artifact status")

if "PHYSICAL_FIELD_DATA_FINITE_SAMPLES_2026_05_28" not in artifact.read_text():
    raise SystemExit("missing dependency on physical field data finite samples")

required_boundaries = [
    "PhysicalDetectorFieldExtractionMap",
    "extractPhysicalDetectorWitness",
    "DetectorBudgetCompatible",
    "coverage of physical field data",
    "disjointness of detector cells",
    "geometric partition correctness",
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

print("FINITE_DETECTOR_PARTITION_OK")
