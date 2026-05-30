#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/mascon_unit_equivalence_certificate_2026_05_30.json"
DOC = ROOT / "docs/status/MASCON_UNIT_EQUIVALENCE_CERTIFICATE_2026_05_30.md"
LEAN = ROOT / "lean/Chronos/Frontier/MasconUnitEquivalenceCertificate.lean"

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    cert = artifact["certificate"]
    boundary = artifact["boundary"]

    assert artifact["object"] == "MASCON_UNIT_EQUIVALENCE_CERTIFICATE_2026_05_30"
    assert artifact["status"] == "CERTIFICATE_RECORDED_TIME_DEPENDENT_OPERATOR_NOT_CLOSED"
    assert "AUTHENTIC_MASCON_COMPARISON_METRIC_2026_05_30" in artifact["depends_on"]
    assert "SOURCE_GRID_TO_MASCON_GRID_UNIT_CONVERSION_LAW_2026_05_30" in artifact["depends_on"]

    assert cert["conversion_law_recorded"] is True
    assert cert["authentic_comparison_metric_recorded"] is True
    assert math.isfinite(cert["conversion_factor"])
    assert cert["conversion_factor"] == 1.0
    assert cert["same_physical_dimension"] is True
    assert cert["mascon_unit_equivalence_certificate_supplied"] is True
    assert cert["time_dependent_source_to_mascon_operator_closed"] is False
    assert cert["empirical_comparison_executed"] is False

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

    assert artifact["next_admissible_object"] == "TIME_DEPENDENT_SOURCE_TO_MASCON_OPERATOR"

    doc = DOC.read_text(encoding="utf-8")
    assert "CERTIFICATE_RECORDED_TIME_DEPENDENT_OPERATOR_NOT_CLOSED" in doc
    assert "No empirical gravity result" in doc

    lean = LEAN.read_text(encoding="utf-8")
    assert "masconUnitEquivalenceCertificate_supplied" in lean
    assert "masconUnitEquivalenceCertificate_timeDependentOperatorOpen" in lean

    print("MASCON_UNIT_EQUIVALENCE_CERTIFICATE_OK")

if __name__ == "__main__":
    main()
