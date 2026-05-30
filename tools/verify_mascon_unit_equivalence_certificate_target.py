#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/mascon_unit_equivalence_certificate_target_2026_05_30.json"
DOC = ROOT / "docs/status/MASCON_UNIT_EQUIVALENCE_CERTIFICATE_TARGET_2026_05_30.md"
LEAN = ROOT / "lean/Chronos/Frontier/MasconUnitEquivalenceCertificateTarget.lean"

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    target = artifact["target"]
    boundary = artifact["boundary"]

    assert artifact["object"] == "MASCON_UNIT_EQUIVALENCE_CERTIFICATE_TARGET_2026_05_30"
    assert artifact["status"] == "TARGET_RECORDED_CERTIFICATE_NOT_SUPPLIED"

    assert "SOURCE_TO_MASCON_OPERATOR_AUDIT_2026_05_30" in artifact["depends_on"]
    assert "PHYSICAL_UNITS_CALIBRATED_SOURCE_TO_MASCON_OPERATOR_2026_05_30" in artifact["depends_on"]

    assert target["source_to_mascon_operator_audit_recorded"] is True
    assert target["physical_units_operator_recorded"] is True
    assert target["finite_physical_vector_statistics_verified"] is True
    assert target["physical_grid_units_bound"] is True
    assert target["physical_grid_units"] == "mGal radial gravity disturbance proxy"

    assert target["mascon_grid_units_bound"] is False
    assert target["unit_conversion_law_supplied"] is False
    assert target["mascon_unit_equivalence_certificate_supplied"] is False
    assert target["authentic_comparison_metric_supplied"] is False
    assert target["time_dependent_source_to_mascon_operator_closed"] is False

    for key in [
        "empirical_gravity_result_claimed",
        "general_relativity_failure_claimed",
        "new_gravity_claimed",
        "dark_matter_replacement_claimed",
        "lambda_cdm_failure_claimed",
        "quantum_gravity_claimed",
        "clay_problem_claimed",
    ]:
        assert boundary[key] is False, key

    assert "MASCON_GRID_UNIT_DECLARATION" in artifact["weakest_missing_inputs"]
    assert "SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW" in artifact["weakest_missing_inputs"]
    assert "AUTHENTIC_MASCON_COMPARISON_METRIC" in artifact["weakest_missing_inputs"]

    assert artifact["next_admissible_object"] == (
        "MASCON_GRID_UNIT_DECLARATION_OR_SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW"
    )

    doc = DOC.read_text(encoding="utf-8")
    assert "TARGET_RECORDED_CERTIFICATE_NOT_SUPPLIED" in doc
    assert "No empirical gravity result" in doc

    lean = LEAN.read_text(encoding="utf-8")
    assert "masconUnitEquivalenceCertificateTarget_notSupplied" in lean
    assert "masconUnitEquivalenceCertificateTarget_noEmpiricalGravityResult" in lean

    print("MASCON_UNIT_EQUIVALENCE_CERTIFICATE_TARGET_OK")

if __name__ == "__main__":
    main()
