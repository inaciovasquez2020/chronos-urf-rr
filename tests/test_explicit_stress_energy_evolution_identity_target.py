import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/explicit_stress_energy_evolution_identity_target_2026_05_22.json"
DOC = ROOT / "docs/status/EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET_2026_05_22.md"

def test_target_status_only():
    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET"
    assert data["status"] == "CONDITIONAL_TENSOR_CALCULATION_TARGET_ONLY"

def test_target_depends_on_wec_pointwise_positivity():
    data = json.loads(ARTIFACT.read_text())
    assert "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL" in data["depends_on"]

def test_required_inputs_are_recorded():
    data = json.loads(ARTIFACT.read_text())
    assert "3_PLUS_1_EINSTEIN_SCALAR_STRESS_ENERGY_TENSOR_COMPONENTS" in data["required_inputs"]
    assert "LAPSE_SHIFT_GAUGE_CONVENTION" in data["required_inputs"]
    assert "COVARIANT_DIVERGENCE_IDENTITY" in data["required_inputs"]
    assert "CURVATURE_COUPLING_TERM_SIGN_CHECK" in data["required_inputs"]
    assert "BOUNDARY_FLUX_TERM_CHECK" in data["required_inputs"]

def test_blockers_are_explicit():
    data = json.loads(ARTIFACT.read_text())
    assert "TENSOR_CALCULATION_NOT_COMPLETED" in data["current_blockers"]
    assert "GAUGE_TERM_CHECK_NOT_COMPLETED" in data["current_blockers"]
    assert "BOUNDARY_FLUX_CONTROL_NOT_PROVED" in data["current_blockers"]

def test_no_theorem_promotion_boundaries():
    data = json.loads(ARTIFACT.read_text())
    does_not_prove = "\n".join(data["does_not_prove"])
    assert "stress-energy evolution identity" in does_not_prove
    assert "WEC preservation under time evolution" in does_not_prove
    assert "finite-time collapse theorem" in does_not_prove
    assert "unrestricted gravity closure" in does_not_prove
    assert "cosmic censorship" in does_not_prove
    assert "hoop conjecture" in does_not_prove
    assert "any Clay problem" in does_not_prove

def test_status_doc_records_next_object():
    text = DOC.read_text()
    assert "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION" in text
    assert "does not supply the tensor calculation" in text
    assert "does not prove WEC preservation under time evolution" in text
