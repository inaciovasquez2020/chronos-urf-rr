import json
from pathlib import Path

ART = Path("artifacts/chronos/empty_active_detector_default_policy_2026_05_28.json")
DOC = Path("docs/status/EMPTY_ACTIVE_DETECTOR_DEFAULT_POLICY_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/EmptyActiveDetectorDefaultPolicy.lean")

def test_artifact_status_dependencies_and_boundaries():
    data = json.loads(ART.read_text())
    assert data["status"] == "SOLVED_RESTRICTED_EMPTY_ACTIVE_DETECTOR_DEFAULT_POLICY_ONLY"
    assert "COMPUTED_ACTIVE_RADIUS_MINIMUM_2026_05_28" in data["depends_on"]
    assert "finiteDetectorExtraction_no_active_default_gate" in data["proved_objects"]
    assert "Clay problem solved" in data["does_not_prove"]

def test_doc_records_scope_and_boundary():
    text = DOC.read_text()
    assert "Status: `SOLVED_RESTRICTED_EMPTY_ACTIVE_DETECTOR_DEFAULT_POLICY_ONLY`." in text
    assert "no detector is active" in text
    assert "This does not prove:" in text
    assert "unrestricted QL_CollapseGate" in text
    assert "solves P vs NP" in text

def test_lean_contains_default_policy_bridge():
    text = LEAN.read_text()
    assert "import Chronos.Frontier.ComputedActiveRadiusMinimum" in text
    assert "def defaultActiveRadiusFloor" in text
    assert "theorem defaultActiveRadiusFloor_eq_computed_of_nonempty" in text
    assert "theorem defaultActiveRadiusFloor_eq_zero_of_empty" in text
    assert "theorem activeRadiusValues_empty_of_no_active" in text
    assert "theorem activeMass_eq_zero_of_no_active" in text
    assert "theorem finiteDetectorExtraction_no_active_default_gate" in text
    assert "sorry" not in text
    assert "admit" not in text
    assert "axiom" not in text
