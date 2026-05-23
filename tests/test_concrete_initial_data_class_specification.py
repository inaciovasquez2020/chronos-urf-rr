import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_concrete_initial_data_class_specification_boundary():
    data = json.loads((ROOT / "artifacts/chronos/concrete_initial_data_class_specification_2026_05_23.json").read_text())
    assert data["status"] == "INITIAL_DATA_CLASS_SPECIFICATION_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["spacetime_dimension"] == 4
    assert data["spatial_dimension"] == 3
    assert "six-field admissibility predicate" in data["required_fields"]
    assert "SixFieldAnalyticPackageHypothesis" in data["blocked_use"]
    assert "any Clay problem" in data["blocked_use"]
    assert data["next_admissible_object"] == "ConcreteMatterModelSpecification"
