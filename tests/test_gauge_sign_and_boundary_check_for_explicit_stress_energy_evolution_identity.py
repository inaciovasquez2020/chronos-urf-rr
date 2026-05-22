import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/gauge_sign_and_boundary_check_for_explicit_stress_energy_evolution_identity_2026_05_22.json"
DOC = ROOT / "docs/status/GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_2026_05_22.md"

def test_status_is_check_surface_only():
    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY"
    assert data["status"] == "GAUGE_SIGN_BOUNDARY_CHECK_RECORDED_CONDITIONAL_NO_IDENTITY_PROMOTION"

def test_dependencies_are_recorded():
    data = json.loads(ARTIFACT.read_text())
    assert "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL" in data["depends_on"]
    assert "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET" in data["depends_on"]
    assert "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION" in data["depends_on"]

def test_fixed_conventions_are_recorded():
    data = json.loads(ARTIFACT.read_text())
    assert data["fixed_conventions"]["signature"] == "(-,+,+,+)"
    assert "n^a n_a = -1" in data["fixed_conventions"]["normal"]
    assert "partial_t = N n + beta" in data["fixed_conventions"]["evolution_flow"]
    assert "K_ij = -1/2 Lie_n gamma_ij" in data["fixed_conventions"]["extrinsic_curvature_sign_lock"]

def test_candidate_identity_is_not_promoted():
    data = json.loads(ARTIFACT.read_text())
    candidate = data["candidate_identity_under_selected_conventions"]
    assert candidate["status"] == "CANDIDATE_SHAPE_RECORDED_NOT_THEOREM"
    assert "n^a nabla_a rho" in candidate["normal_projected_shape"]
    assert "partial_t - Lie_beta" in candidate["coordinate_shape"]

def test_gauge_and_boundary_checks_are_retained():
    data = json.loads(ARTIFACT.read_text())
    gauge = "\n".join(data["gauge_checks"])
    boundary = "\n".join(data["boundary_flux_checks"])
    assert "no gauge term is discarded" in gauge
    assert "boundary contribution integral over partial Omega is not assumed to vanish" in boundary
    assert "asymptotically flat flux vanishing is not assumed" in boundary
    assert "periodic-boundary cancellation is not assumed" in boundary

def test_remaining_blockers_are_explicit():
    data = json.loads(ARTIFACT.read_text())
    assert "EXTRINSIC_CURVATURE_SIGN_CONVENTION_NOT_EXTERNALLY_DISCHARGED" in data["remaining_blockers"]
    assert "BOUNDARY_FLUX_VANISHING_NOT_PROVED" in data["remaining_blockers"]
    assert "CANDIDATE_IDENTITY_NOT_LEAN_FORMALIZED_AS_TENSOR_THEOREM" in data["remaining_blockers"]
    assert "NO_WEC_PRESERVATION_THEOREM" in data["remaining_blockers"]
    assert "NO_CONTINUATION_CRITERION" in data["remaining_blockers"]

def test_no_theorem_promotion_boundaries():
    data = json.loads(ARTIFACT.read_text())
    does_not_prove = "\n".join(data["does_not_prove"])
    assert "unconditional stress-energy evolution identity" in does_not_prove
    assert "WEC preservation under time evolution" in does_not_prove
    assert "energy estimate dE/dt <= C E" in does_not_prove
    assert "finite-time collapse theorem" in does_not_prove
    assert "unrestricted gravity closure" in does_not_prove
    assert "cosmic censorship" in does_not_prove
    assert "hoop conjecture" in does_not_prove
    assert "any Clay problem" in does_not_prove

def test_status_doc_records_next_object():
    text = DOC.read_text()
    assert "LEAN_FORMAL_STRESS_ENERGY_IDENTITY_OR_EXTERNAL_TENSOR_AUDIT" in text
    assert "does not prove WEC preservation under time evolution" in text
    assert "does not prove finite-time collapse" in text
