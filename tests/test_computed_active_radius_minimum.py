import json
from pathlib import Path

ART = Path("artifacts/chronos/computed_active_radius_minimum_2026_05_28.json")
DOC = Path("docs/status/COMPUTED_ACTIVE_RADIUS_MINIMUM_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/ComputedActiveRadiusMinimum.lean")

def test_artifact_status_dependencies_and_boundaries():
    data = json.loads(ART.read_text())
    assert data["status"] == "SOLVED_RESTRICTED_COMPUTED_ACTIVE_RADIUS_MINIMUM_ONLY"
    assert "RESTRICTED_QL_FINITE_DETECTOR_MASS_RADIUS_EXTRACTION_2026_05_28" in data["depends_on"]
    assert "computedActiveRadiusMinimum_le_active_radius" in data["proved_objects"]
    assert "finiteDetectorExtraction_gate_of_computed_min_le_mass" in data["proved_objects"]
    assert "Clay problem solved" in data["does_not_prove"]

def test_doc_records_scope_and_boundary():
    text = DOC.read_text()
    assert "Status: `SOLVED_RESTRICTED_COMPUTED_ACTIVE_RADIUS_MINIMUM_ONLY`." in text
    assert "Finset.min'" in text
    assert "This does not prove:" in text
    assert "unrestricted QL_CollapseGate" in text
    assert "solves P vs NP" in text

def test_lean_contains_computed_minimum_bridge():
    text = LEAN.read_text()
    assert "import Chronos.Frontier.RestrictedQLFiniteDetectorMassRadiusExtraction" in text
    assert "def activeDetectors" in text
    assert "def activeRadiusValues" in text
    assert "def computedActiveRadiusMinimum" in text
    assert "Finset.min'" in text
    assert "theorem active_radius_mem_values_of_active" in text
    assert "theorem computedActiveRadiusMinimum_le_active_radius" in text
    assert "theorem finiteDetectorExtraction_gate_of_computed_min_le_mass" in text
    assert "theorem finiteDetectorExtraction_computed_min_gate_mono_mass" in text
    assert "sorry" not in text
    assert "admit" not in text
    assert "axiom" not in text
