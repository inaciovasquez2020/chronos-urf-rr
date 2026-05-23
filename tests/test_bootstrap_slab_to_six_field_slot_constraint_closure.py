import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_bootstrap_slab_to_six_field_slot_constraint_closure_boundary():
    data = json.loads((ROOT / "artifacts/chronos/bootstrap_slab_to_six_field_slot_constraint_closure_2026_05_23.json").read_text())
    assert data["status"] == "STRUCTURAL_DEPENDENCY_DAG_VALIDATOR_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["closed_surface"] == "BootstrapSlabToSixFieldSlotConstraintClosure"
    assert "BootstrapSlabInductionKernel" in data["included_interfaces"]
    assert "BootstrapSlabToSixFieldSlotCompatibilityMatrix" in data["included_interfaces"]
    assert "BootstrapSlabToSixFieldSlotConstraintClosure" in data["included_interfaces"]
    assert "continuationAlternativeSlot -> collapseGateTriggerSlot" in data["dependency_edges"]
    assert "SixFieldAnalyticPackageHypothesis" in data["blocked_use"]
    assert "any Clay problem" in data["blocked_use"]
    assert data["next_admissible_object"] == "AnalyticEstimateCandidatePacket"
