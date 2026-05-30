#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/mascon_grid_unit_declaration_2026_05_30.json"
DOC = ROOT / "docs/status/MASCON_GRID_UNIT_DECLARATION_2026_05_30.md"
LEAN = ROOT / "lean/Chronos/Frontier/MasconGridUnitDeclaration.lean"

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    decl = artifact["declaration"]
    boundary = artifact["boundary"]

    assert artifact["object"] == "MASCON_GRID_UNIT_DECLARATION_2026_05_30"
    assert artifact["status"] == "DECLARATION_RECORDED_CONVERSION_LAW_NOT_SUPPLIED"
    assert "MASCON_UNIT_EQUIVALENCE_CERTIFICATE_TARGET_2026_05_30" in artifact["depends_on"]

    assert decl["unit_equivalence_target_recorded"] is True
    assert decl["physical_grid_units_bound"] is True
    assert decl["physical_grid_units"] == "mGal radial gravity disturbance proxy"
    assert decl["mascon_grid_units_declared"] is True
    assert decl["mascon_grid_units"] == "mGal-equivalent radial gravity disturbance on MASCON comparison grid"

    assert decl["source_grid_to_mascon_grid_conversion_law_supplied"] is False
    assert decl["authentic_comparison_metric_supplied"] is False
    assert decl["mascon_unit_equivalence_certificate_supplied"] is False
    assert decl["time_dependent_source_to_mascon_operator_closed"] is False

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
        "SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW",
        "AUTHENTIC_MASCON_COMPARISON_METRIC",
        "MASCON_UNIT_EQUIVALENCE_CERTIFICATE",
    ]
    assert artifact["next_admissible_object"] == "SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW"

    doc = DOC.read_text(encoding="utf-8")
    assert "DECLARATION_RECORDED_CONVERSION_LAW_NOT_SUPPLIED" in doc
    assert "No empirical gravity result" in doc

    lean = LEAN.read_text(encoding="utf-8")
    assert "masconGridUnitDeclaration_declared" in lean
    assert "masconGridUnitDeclaration_conversionLawNotSupplied" in lean

    print("MASCON_GRID_UNIT_DECLARATION_OK")

if __name__ == "__main__":
    main()
