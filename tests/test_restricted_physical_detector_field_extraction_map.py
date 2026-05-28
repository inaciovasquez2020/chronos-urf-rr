import json
import subprocess
from pathlib import Path

def test_verifier_passes():
    out = subprocess.check_output([
        "python3",
        "tools/verify_restricted_physical_detector_field_extraction_map.py",
    ], text=True)
    assert "RESTRICTED_PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_OK" in out

def test_artifact_is_conditional_and_boundary_safe():
    data = json.loads(Path(
        "artifacts/chronos/restricted_physical_detector_field_extraction_map_2026_05_28.json"
    ).read_text())
    assert data["status"] == "CONDITIONAL_RESTRICTED_INTERFACE_BRIDGE_SOLVED"
    assert "PhysicalDetectorFieldAdmissible.gate_bound" in data["conditional_on"]
    assert "derivation of gate_bound from raw physical readings" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]

def test_doc_records_false_pointwise_route():
    text = Path(
        "docs/status/RESTRICTED_PHYSICAL_DETECTOR_FIELD_EXTRACTION_MAP_2026_05_28.md"
    ).read_text()
    assert "does not imply" in text
    assert "false local-to-global aggregation route" in text
    assert "Corrected Boundary Admissibility" in text
