import json
from pathlib import Path

ART = Path("artifacts/chronos/restricted_ql_mass_radius_gate_monotonicity_2026_05_28.json")
DOC = Path("docs/status/RESTRICTED_QL_MASS_RADIUS_GATE_MONOTONICITY_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/RestrictedQLMassRadiusGateMonotonicity.lean")

def test_artifact_status_and_boundaries():
    data = json.loads(ART.read_text())
    assert data["status"] == "SOLVED_RESTRICTED_LOCAL_ARITHMETIC_GATE_ONLY"
    assert "restrictedQLCollapseGate_mono_massRadius" in data["proved_objects"]
    assert "restrictedQLCollapseGate_zero_mass_rigid" in data["proved_objects"]
    assert "cosmic censorship proved" in data["does_not_prove"]
    assert "hoop conjecture proved" in data["does_not_prove"]
    assert "Clay problem solved" in data["does_not_prove"]

def test_doc_records_boundary():
    text = DOC.read_text()
    assert "Status: `SOLVED_RESTRICTED_LOCAL_ARITHMETIC_GATE_ONLY`." in text
    assert "This does not prove:" in text
    assert "unrestricted QL_CollapseGate" in text
    assert "solves P vs NP" in text

def test_lean_contains_solved_local_theorems():
    text = LEAN.read_text()
    assert "theorem restrictedQLCollapseGate_mono_massRadius" in text
    assert "theorem restrictedQLCollapseGate_zero_mass_rigid" in text
    assert "Nat.le_trans" in text
    assert "Nat.eq_zero_of_le_zero" in text
