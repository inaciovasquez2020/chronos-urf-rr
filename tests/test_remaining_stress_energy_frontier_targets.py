import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = [
    "lean_formal_stress_energy_identity_or_external_tensor_audit",
    "unconditional_stress_energy_evolution_identity_target",
    "wec_preservation_under_time_evolution_target",
    "energy_estimate_dedt_le_ce_target",
    "non_symmetric_continuation_criterion_target",
    "finite_time_collapse_theorem_target",
    "unrestricted_gravity_closure_target",
]

def artifact(slug):
    path = ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json"
    return json.loads(path.read_text())

def test_all_remaining_targets_exist():
    for slug in OBJECTS:
        path = ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json"
        assert path.exists()

def test_common_dependencies_are_preserved():
    for slug in OBJECTS:
        data = artifact(slug)
        assert "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL" in data["depends_on"]
        assert "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET" in data["depends_on"]
        assert "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION" in data["depends_on"]
        assert "GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY" in data["depends_on"]

def test_no_theorem_promotion_for_all_targets():
    for slug in OBJECTS:
        data = artifact(slug)
        does_not_prove = "\n".join(data["does_not_prove"])
        assert "unconditional stress-energy evolution identity" in does_not_prove
        assert "WEC preservation under time evolution" in does_not_prove
        assert "energy estimate dE/dt <= C E" in does_not_prove
        assert "finite-time collapse theorem" in does_not_prove
        assert "unrestricted gravity closure" in does_not_prove
        assert "any Clay problem" in does_not_prove

def test_lean_audit_route_module_exists_without_admits():
    path = ROOT / "lean/Chronos/Frontier/LeanFormalStressEnergyIdentityOrExternalTensorAudit.lean"
    text = path.read_text()
    assert "StressEnergyIdentityAuditRoute" in text
    assert "leanFormalStressEnergyIdentityOrExternalTensorAudit_recorded" in text
    assert "sorry" not in text.lower()
    assert "admit" not in text.lower()

def test_unrestricted_gravity_closure_remains_open():
    data = artifact("unrestricted_gravity_closure_target")
    assert data["status"] == "OPEN_TARGET_NO_UNRESTRICTED_GRAVITY_CLOSURE"
    assert "FINITE_TIME_COLLAPSE_THEOREM_NOT_PROVED" in data["remaining_blockers"]
