#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/PhysicalDetectorFieldExtractionMap.lean"
ART = ROOT / "artifacts/chronos/physical_detector_field_extraction_map_2026_05_28.json"
DOC = ROOT / "docs/status/PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_2026_05_28.md"
CHRONOS = ROOT / "lean/Chronos.lean"

for path in [LEAN, ART, DOC, CHRONOS]:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")

lean = LEAN.read_text()
doc = DOC.read_text()
chronos = CHRONOS.read_text()
artifact = json.loads(ART.read_text())

required_lean_tokens = [
    "import Chronos.Frontier.DetectorBudgetCompatibleToGate",
    "structure PhysicalDetectorFieldExtractionMap",
    "compatibilityToGate",
    "PhysicalDetectorFieldExtractionMap.gate_from_compatibility",
    "PhysicalDetectorFieldExtractionMap.witness_from_data_partition",
]

for token in required_lean_tokens:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

if "import Chronos.Frontier.PhysicalDetectorFieldExtractionMap" not in chronos:
    raise SystemExit("missing Chronos import")

if artifact.get("id") != "PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_2026_05_28":
    raise SystemExit("bad artifact id")

if artifact.get("status") != "FINITE_WRAPPER_INTERFACE_ONLY":
    raise SystemExit("bad artifact status")

required_dependencies = [
    "PHYSICAL_FIELD_DATA_FINITE_SAMPLES_2026_05_28",
    "FINITE_DETECTOR_PARTITION_2026_05_28",
    "EXTRACT_PHYSICAL_DETECTOR_WITNESS_2026_05_28",
    "DETECTOR_BUDGET_COMPATIBLE_2026_05_28",
    "DETECTOR_BUDGET_COMPATIBLE_TO_GATE_2026_05_28",
]

for dep in required_dependencies:
    if dep not in artifact.get("depends_on", []):
        raise SystemExit(f"missing dependency: {dep}")

required_doc_tokens = [
    "FINITE_WRAPPER_INTERFACE_ONLY",
    "PhysicalDetectorFieldExtractionMap",
    "DetectorBudgetCompatible to RestrictedFiniteDetectorExtractionGate",
    "finite wrapper/interface only",
    "coverage/disjointness/geometric partition correctness",
    "empirical detector correctness",
    "Einstein-matter PDE well-posedness",
    "cosmic censorship",
    "hoop conjecture",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for token in required_doc_tokens:
    if token not in doc:
        raise SystemExit(f"missing doc token: {token}")

print("PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_OK")
