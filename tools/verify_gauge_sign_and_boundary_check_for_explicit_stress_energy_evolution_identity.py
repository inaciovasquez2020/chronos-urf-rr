#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/gauge_sign_and_boundary_check_for_explicit_stress_energy_evolution_identity_2026_05_22.json"
DOC = ROOT / "docs/status/GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_2026_05_22.md"

REQUIRED_DEPENDENCIES = [
    "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL",
    "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET",
    "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION",
]

REQUIRED_BLOCKERS = [
    "EXTRINSIC_CURVATURE_SIGN_CONVENTION_NOT_EXTERNALLY_DISCHARGED",
    "BOUNDARY_FLUX_VANISHING_NOT_PROVED",
    "CANDIDATE_IDENTITY_NOT_LEAN_FORMALIZED_AS_TENSOR_THEOREM",
    "NO_WEC_PRESERVATION_THEOREM",
    "NO_CONTINUATION_CRITERION",
    "NO_COLLAPSE_TRIGGER_DERIVATION",
]

REQUIRED_DOES_NOT_PROVE = [
    "unconditional stress-energy evolution identity",
    "WEC preservation under time evolution",
    "energy estimate dE/dt <= C E",
    "non-symmetric Einstein-scalar continuation criterion",
    "Raychaudhuri focusing with shear control",
    "non-symmetric trapped-surface trigger from concentration",
    "finite-time collapse theorem",
    "unrestricted gravity closure",
    "cosmic censorship",
    "hoop conjecture",
    "four-dimensional non-symmetric collapse theorem",
    "any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["id"] == "GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY"
    assert data["status"] == "GAUGE_SIGN_BOUNDARY_CHECK_RECORDED_CONDITIONAL_NO_IDENTITY_PROMOTION"
    assert data["next_admissible_object"] == "LEAN_FORMAL_STRESS_ENERGY_IDENTITY_OR_EXTERNAL_TENSOR_AUDIT"

    for dep in REQUIRED_DEPENDENCIES:
        assert dep in data["depends_on"]

    assert data["fixed_conventions"]["signature"] == "(-,+,+,+)"
    assert "K_ij = -1/2 Lie_n gamma_ij" in data["fixed_conventions"]["extrinsic_curvature_sign_lock"]
    assert data["candidate_identity_under_selected_conventions"]["status"] == "CANDIDATE_SHAPE_RECORDED_NOT_THEOREM"

    gauge_checks = "\n".join(data["gauge_checks"])
    assert "lapse acceleration term retained" in gauge_checks
    assert "shift contribution retained" in gauge_checks
    assert "no gauge term is discarded" in gauge_checks

    boundary_checks = "\n".join(data["boundary_flux_checks"])
    assert "not assumed to vanish" in boundary_checks
    assert "asymptotically flat flux vanishing is not assumed" in boundary_checks
    assert "compact-without-boundary cancellation is not assumed" in boundary_checks
    assert "periodic-boundary cancellation is not assumed" in boundary_checks

    for blocker in REQUIRED_BLOCKERS:
        assert blocker in data["remaining_blockers"]
        assert blocker in doc

    does_not_prove = "\n".join(data["does_not_prove"])
    for token in REQUIRED_DOES_NOT_PROVE:
        assert token in does_not_prove

    assert "does not prove WEC preservation under time evolution" in doc
    assert "does not prove finite-time collapse" in doc

    print("Gauge sign and boundary check verification OK.")
    print("Status: GAUGE_SIGN_BOUNDARY_CHECK_RECORDED_CONDITIONAL_NO_IDENTITY_PROMOTION")
    print("Next admissible object: LEAN_FORMAL_STRESS_ENERGY_IDENTITY_OR_EXTERNAL_TENSOR_AUDIT")

if __name__ == "__main__":
    main()
