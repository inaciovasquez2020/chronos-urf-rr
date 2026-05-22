#!/usr/bin/env python3
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

REQUIRED_DEPS = [
    "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL",
    "EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_TARGET",
    "FILLED_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY_CALCULATION",
    "GAUGE_SIGN_AND_BOUNDARY_CHECK_FOR_EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY",
]

REQUIRED_DOES_NOT_PROVE = [
    "unconditional stress-energy evolution identity",
    "WEC preservation under time evolution",
    "energy estimate dE/dt <= C E",
    "finite-time collapse theorem",
    "unrestricted gravity closure",
    "any Clay problem",
]

def main() -> None:
    for slug in OBJECTS:
        artifact_path = ROOT / "artifacts/chronos" / f"{slug}_2026_05_22.json"
        assert artifact_path.exists(), artifact_path
        data = json.loads(artifact_path.read_text())

        assert data["repository"] == "chronos-urf-rr"
        assert "TARGET" in data["status"] or "AUDIT" in data["status"] or "OPEN" in data["status"]

        for dep in REQUIRED_DEPS:
            assert dep in data["depends_on"]

        does_not_prove = "\n".join(data["does_not_prove"])
        for token in REQUIRED_DOES_NOT_PROVE:
            assert token in does_not_prove

        boundary = "\n".join(data["boundary"])
        assert "no theorem promotion" in boundary
        assert "no unrestricted gravity closure" in boundary

    lean_path = ROOT / "lean/Chronos/Frontier/LeanFormalStressEnergyIdentityOrExternalTensorAudit.lean"
    lean_text = lean_path.read_text()
    assert "leanFormalStressEnergyIdentityOrExternalTensorAudit_recorded" in lean_text
    assert "sorry" not in lean_text.lower()
    assert "admit" not in lean_text.lower()

    print("Remaining stress-energy frontier targets verification OK.")
    print("Status: TARGETS_RECORDED_NO_THEOREM_PROMOTION")
    print("Next admissible object: SELECT_AUDIT_ROUTE_LEAN_FORMAL_OR_EXTERNAL_TENSOR")

if __name__ == "__main__":
    main()
