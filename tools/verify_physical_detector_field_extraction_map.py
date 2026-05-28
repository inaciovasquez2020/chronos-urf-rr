import json
from pathlib import Path

ART = Path("artifacts/chronos/physical_detector_field_extraction_map_2026_05_28.json")
DOC = Path("docs/status/PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/PhysicalDetectorFieldExtractionMap.lean")

required = [
    "PDE well-posedness",
    "collapse theorem",
    "cosmic censorship",
    "hoop conjecture",
    "unrestricted QL_CollapseGate",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["status"] == "RESTRICTED_INTERFACE_GATE_COMPATIBILITY_ONLY"
assert data["object"] == "PhysicalDetectorFieldExtractionMap"
for token in required:
    assert token in doc
    assert token in data["does_not_prove"]
for token in [
    "physical_detector_field_feeds_restricted_gate",
    "empty_physical_detector_field_zero_active_mass",
]:
    assert token in lean

print("PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_OK")
