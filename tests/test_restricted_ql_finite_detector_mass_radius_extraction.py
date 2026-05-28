import json
from pathlib import Path
ART = Path("artifacts/chronos/restricted_ql_finite_detector_mass_radius_extraction_2026_05_28.json")
DOC = Path("docs/status/RESTRICTED_QL_FINITE_DETECTOR_MASS_RADIUS_EXTRACTION_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/RestrictedQLFiniteDetectorMassRadiusExtraction.lean")

def test_artifact_status_and_dependency():
    data = json.loads(ART.read_text())
    assert data["status"] == "SOLVED_RESTRICTED_FINITE_DETECTOR_EXTRACTION_BRIDGE_ONLY"
    assert "RESTRICTED_QL_MASS_RADIUS_GATE_MONOTONICITY_2026_05_28" in data["depends_on"]
    assert "finiteDetectorExtraction_gate_mono_mass" in data["proved_objects"]

def test_doc_records_boundary():
    text = DOC.read_text()
    assert "This does not prove:" in text
    assert "unrestricted QL_CollapseGate" in text
    assert "solves P vs NP" in text
    assert "Clay problem solved" in text

def test_lean_contains_solved_bridge():
    text = LEAN.read_text()
    assert "import Chronos.Frontier.RestrictedQLMassRadiusGateMonotonicity" in text
    assert "def activeMass" in text
    assert "def finiteDetectorMassRadiusExtraction" in text
    assert "theorem finiteDetectorExtraction_gate_of_active_floor_le_mass" in text
    assert "theorem finiteDetectorExtraction_activeMass_mono" in text
    assert "theorem finiteDetectorExtraction_gate_mono_mass" in text
    assert "Finset.sum_le_sum" in text
    assert "Nat.le_trans" in text
    assert "sorry" not in text
    assert "admit" not in text
    assert "axiom" not in text
