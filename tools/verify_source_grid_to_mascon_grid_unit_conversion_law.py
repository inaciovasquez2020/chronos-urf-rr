#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/source_grid_to_mascon_grid_unit_conversion_law_2026_05_30.json"
DOC = ROOT / "docs/status/SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW_2026_05_30.md"
LEAN = ROOT / "lean/Chronos/Frontier/SourceGridToMasconGridUnitConversionLaw.lean"

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    law = artifact["conversion_law"]
    boundary = artifact["boundary"]

    assert artifact["object"] == "SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW_2026_05_30"
    assert artifact["status"] == "CONVERSION_LAW_RECORDED_CERTIFICATE_NOT_SUPPLIED"
    assert "MASCON_GRID_UNIT_DECLARATION_2026_05_30" in artifact["depends_on"]

    assert law["mascon_grid_unit_declaration_recorded"] is True
    assert law["source_grid_units"] == "mGal radial gravity disturbance proxy"
    assert law["mascon_grid_units"] == "mGal-equivalent radial gravity disturbance on MASCON comparison grid"
    assert law["conversion_law_supplied"] is True
    assert math.isfinite(law["conversion_factor"])
    assert law["conversion_factor"] == 1.0
    assert law["conversion_factor_units"] == "mGal-equivalent per mGal"
    assert law["dimension_preserving"] is True
    assert law["grid_shape_projection_only"] is True
    assert law["source_to_mascon_numeric_identity_after_unit_declaration"] is True

    assert law["authentic_comparison_metric_supplied"] is False
    assert law["mascon_unit_equivalence_certificate_supplied"] is False
    assert law["time_dependent_source_to_mascon_operator_closed"] is False

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

    assert artifact["weakest_missing_inputs"] == [
        "AUTHENTIC_MASCON_COMPARISON_METRIC",
        "MASCON_UNIT_EQUIVALENCE_CERTIFICATE",
        "TIME_DEPENDENT_SOURCE_TO_MASCON_OPERATOR",
    ]
    assert artifact["next_admissible_object"] == (
        "AUTHENTIC_MASCON_COMPARISON_METRIC_OR_MASCON_UNIT_EQUIVALENCE_CERTIFICATE"
    )

    doc = DOC.read_text(encoding="utf-8")
    assert "CONVERSION_LAW_RECORDED_CERTIFICATE_NOT_SUPPLIED" in doc
    assert "No empirical gravity result" in doc

    lean = LEAN.read_text(encoding="utf-8")
    assert "sourceGridToMasconGridUnitConversionLaw_supplied" in lean
    assert "sourceGridToMasconGridUnitConversionLaw_certificateNotSupplied" in lean

    print("SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW_OK")

if __name__ == "__main__":
    main()
