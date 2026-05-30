#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/gravity/source_to_mascon_operator_audit_2026_05_30.json"
DOC = ROOT / "docs/status/SOURCE_TO_MASCON_OPERATOR_AUDIT_2026_05_30.md"
LEAN = ROOT / "lean/Chronos/Frontier/SourceToMasconOperatorAudit.lean"

def main() -> None:
    artifact = json.loads(ART.read_text(encoding="utf-8"))
    audit = artifact["audit"]

    assert artifact["object"] == "SOURCE_TO_MASCON_OPERATOR_AUDIT_2026_05_30"
    assert artifact["status"] == "AUDIT_RECORDED_NO_MASCON_UNIT_EQUIVALENCE_CLOSURE"

    assert audit["physical_units_operator_recorded"] is True
    assert audit["finite_physical_vector_statistics_verified"] is True
    assert audit["source_to_mascon_shape_operator_recorded"] is True
    assert audit["source_to_mascon_operator_audit_recorded"] is True

    assert audit["mascon_unit_equivalence_closed"] is False
    assert audit["time_dependent_source_to_mascon_operator_closed"] is False

    forbidden = [
        "empirical_gravity_result_claimed",
        "general_relativity_failure_claimed",
        "new_gravity_claimed",
        "dark_matter_replacement_claimed",
        "lambda_cdm_failure_claimed",
        "quantum_gravity_claimed",
        "clay_problem_claimed",
    ]
    for key in forbidden:
        assert audit[key] is False, key

    assert "MASCON_UNIT_EQUIVALENCE_CERTIFICATE" in artifact["weakest_missing_inputs"]
    assert "TIME_DEPENDENT_SOURCE_TO_MASCON_OPERATOR" in artifact["weakest_missing_inputs"]
    assert artifact["next_admissible_object"] == (
        "MASCON_UNIT_EQUIVALENCE_CERTIFICATE_OR_TIME_DEPENDENT_SOURCE_TO_MASCON_OPERATOR"
    )

    doc = DOC.read_text(encoding="utf-8")
    assert "No empirical gravity result" in doc
    assert "MASCON unit equivalence" in doc

    lean = LEAN.read_text(encoding="utf-8")
    assert "sourceToMasconOperatorAudit_noEmpiricalGravityResult" in lean
    assert "sourceToMasconOperatorAudit_masconUnitEquivalenceOpen" in lean

    print("SOURCE_TO_MASCON_OPERATOR_AUDIT_OK")

if __name__ == "__main__":
    main()
