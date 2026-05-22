import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/filled_explicit_stress_energy_evolution_identity_calculation_2026_05_22.json"
DOC = ROOT / "docs/status/FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION_2026_05_22.md"

def test_filled_calculation_status():
    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION"
    assert data["status"] == "FORMULA_PAYLOAD_FILLED_CONDITIONAL_NO_EVOLUTION_THEOREM"

def test_dependencies_are_recorded():
    data = json.loads(ARTIFACT.read_text())
    assert "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL" in data["depends_on"]
    assert "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET" in data["depends_on"]

def test_scalar_stress_energy_components_are_filled():
    data = json.loads(ARTIFACT.read_text())
    components = data["three_plus_one_components"]
    assert "rho" in components
    assert "j_i" in components
    assert "S_ij" in components
    assert "trace_S" in components
    assert "V(phi)" in components["rho"]
    assert "- Pi D_i phi" in components["j_i"]

def test_candidate_identity_is_sign_locked():
    data = json.loads(ARTIFACT.read_text())
    assert data["candidate_energy_projection"]["sign_status"] == "SIGN_CONVENTION_DEPENDENT_REQUIRES_VERIFICATION"
    assert "K_ij S^ij" in data["candidate_energy_projection"]["candidate_form"]
    assert "D_i log N" in data["candidate_energy_projection"]["lapse_acceleration"]

def test_remaining_blockers_are_recorded():
    data = json.loads(ARTIFACT.read_text())
    assert "SIGN_CONVENTION_CHECK_NOT_DISCHARGED" in data["remaining_blockers"]
    assert "GAUGE_TERM_CHECK_NOT_DISCHARGED" in data["remaining_blockers"]
    assert "BOUNDARY_FLUX_CONTROL_NOT_PROVED" in data["remaining_blockers"]
    assert "CANDIDATE_IDENTITY_NOT_LEAN_FORMALIZED" in data["remaining_blockers"]
    assert "NO_WEC_PRESERVATION_THEOREM" in data["remaining_blockers"]

def test_no_theorem_promotion_boundaries():
    data = json.loads(ARTIFACT.read_text())
    does_not_prove = "\n".join(data["does_not_prove"])
    assert "unconditional stress-energy evolution identity" in does_not_prove
    assert "WEC preservation under time evolution" in does_not_prove
    assert "finite-time collapse theorem" in does_not_prove
    assert "unrestricted gravity closure" in does_not_prove
    assert "cosmic censorship" in does_not_prove
    assert "hoop conjecture" in does_not_prove
    assert "any Clay problem" in does_not_prove

def test_status_doc_records_next_admissible_object():
    text = DOC.read_text()
    assert "GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY" in text
    assert "does not prove WEC preservation under time evolution" in text
    assert "does not prove finite-time collapse" in text
