#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/authentic_mascon_comparison_metric_2026_05_30.json"
DOC = ROOT / "docs/status/AUTHENTIC_MASCON_COMPARISON_METRIC_2026_05_30.md"
LEAN = ROOT / "lean/Chronos/Frontier/AuthenticMasconComparisonMetric.lean"

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    metric = artifact["metric"]
    boundary = artifact["boundary"]

    assert artifact["object"] == "AUTHENTIC_MASCON_COMPARISON_METRIC_2026_05_30"
    assert artifact["status"] == "METRIC_RECORDED_NO_EMPIRICAL_RESULT"
    assert "SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW_2026_05_30" in artifact["depends_on"]

    assert metric["conversion_law_recorded"] is True
    assert metric["metric_supplied"] is True
    assert metric["same_unit_comparison"] is True
    assert metric["dimension_preserving"] is True
    assert metric["empirical_comparison_executed"] is False

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

    assert artifact["next_admissible_object"] == "MASCON_UNIT_EQUIVALENCE_CERTIFICATE"

    doc = DOC.read_text(encoding="utf-8")
    assert "METRIC_RECORDED_NO_EMPIRICAL_RESULT" in doc
    assert "No empirical gravity result" in doc

    lean = LEAN.read_text(encoding="utf-8")
    assert "authenticMasconComparisonMetric_supplied" in lean
    assert "authenticMasconComparisonMetric_noEmpiricalGravityResult" in lean

    print("AUTHENTIC_MASCON_COMPARISON_METRIC_OK")

if __name__ == "__main__":
    main()
