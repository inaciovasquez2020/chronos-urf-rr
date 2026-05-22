#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/filled_explicit_stress_energy_evolution_identity_calculation_2026_05_22.json"
DOC = ROOT / "docs/status/FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION_2026_05_22.md"

REQUIRED_COMPONENTS = [
    "rho",
    "j_i",
    "S_ij",
    "trace_S",
]

REQUIRED_BLOCKERS = [
    "SIGN_CONVENTION_CHECK_NOT_DISCHARGED",
    "GAUGE_TERM_CHECK_NOT_DISCHARGED",
    "BOUNDARY_FLUX_CONTROL_NOT_PROVED",
    "CANDIDATE_IDENTITY_NOT_LEAN_FORMALIZED",
    "NO_WEC_PRESERVATION_THEOREM",
    "NO_CONTINUATION_CRITERION",
]

REQUIRED_BOUNDARIES = [
    "unconditional stress-energy evolution identity",
    "WEC preservation under time evolution",
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

    assert data["id"] == "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION"
    assert data["status"] == "FORMULA_PAYLOAD_FILLED_CONDITIONAL_NO_EVOLUTION_THEOREM"
    assert data["signature_convention"] == "(-,+,+,+)"
    assert data["next_admissible_object"] == (
        "GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY"
    )

    assert "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL" in data["depends_on"]
    assert "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET" in data["depends_on"]

    for key in REQUIRED_COMPONENTS:
        assert key in data["three_plus_one_components"]

    assert "T_ab" in data["stress_energy_tensor"]["formula"]
    assert "nabla_a T^{ab} = 0" in data["stress_energy_tensor"]["conservation_identity"]
    assert data["candidate_energy_projection"]["sign_status"] == (
        "SIGN_CONVENTION_DEPENDENT_REQUIRES_VERIFICATION"
    )

    for blocker in REQUIRED_BLOCKERS:
        assert blocker in data["remaining_blockers"]
        assert blocker in doc

    does_not_prove = "\n".join(data["does_not_prove"])
    for token in REQUIRED_BOUNDARIES:
        assert token in does_not_prove

    assert "does not prove WEC preservation under time evolution" in doc
    assert "does not prove finite-time collapse" in doc

    print("Filled explicit stress-energy evolution identity calculation verification OK.")
    print("Status: FORMULA_PAYLOAD_FILLED_CONDITIONAL_NO_EVOLUTION_THEOREM")
    print("Next admissible object: GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY")

if __name__ == "__main__":
    main()
