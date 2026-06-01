#!/usr/bin/env python3
import hashlib
import json
import math
import re
from pathlib import Path

ART = Path("artifacts/chronos/non_null_physical_model_vector_or_deficit_mass_derivation_2026_06_01.json")
DOC = Path("docs/status/NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_2026_06_01.md")
TARGET = Path("artifacts/chronos/non_null_physical_model_vector_or_deficit_mass_derivation_target_2026_06_01.json")
BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")

REQUIRED_BOUNDARY = {
    "derived surface mass density from observed LWE baseline only",
    "not an independent predictive DFM-MKC model",
    "not a fitted model",
    "not an empirical validation result",
    "requires a fresh comparison run before any result interpretation",
    "no empirical gravity result claim",
    "no anomaly detection claim",
    "no model-favored result claim",
    "no baseline-favored result claim",
    "no DFM-MKC validation",
    "no Lambda-CDM failure",
    "no dark matter resolution",
    "no dark energy resolution",
    "no physical discovery claim",
    "no Chronos-RR closure",
    "no H4.1/FGL closure",
    "no P vs NP claim",
    "no Clay-problem claim",
}

FORBIDDEN_CLAIMS = [
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "ANOMALY_DETECTED_TRUE",
    "MODEL_FAVORED_RESULT_CLAIMED_TRUE",
    "BASELINE_FAVORED_RESULT_CLAIMED_TRUE",
    "DFM_MKC_VALIDATED_TRUE",
    "LAMBDA_CDM_FAILED_TRUE",
    "CLAY_CLOSED_TRUE"
]

def check_vector_sha(vec, key):
    values = vec["values"]
    assert vec["vector_length"] == len(values)
    assert vec["vector_length"] > 0
    assert all(math.isfinite(float(x)) for x in values)
    assert re.fullmatch(r"[0-9a-f]{64}", vec[key])
    text = "\n".join(f"{float(x):.12g}" for x in values) + "\n"
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == vec[key]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert TARGET.exists(), f"missing target: {TARGET}"
    assert BASELINE.exists(), f"missing baseline: {BASELINE}"

    data = json.loads(ART.read_text())
    target = json.loads(TARGET.read_text())
    baseline = json.loads(BASELINE.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_2026_06_01"
    assert data["object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION"
    assert data["status"] == "NON_NULL_SURFACE_MASS_DENSITY_DERIVATION_SUPPLIED_FROM_AUTHENTICATED_LWE_BASELINE_NO_EMPIRICAL_CLAIM"
    assert data["decision"] == "PASS"

    assert target["object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_TARGET"
    assert baseline["object"] == "BASELINE_GRAVITY_VECTOR"

    assert data["target_required_input_supplied"] is True
    assert data["resolved_missing_input"] == "NonNullPhysicalModelVectorOrDeficitMassDerivation"

    vec = data["non_null_physical_model_vector_or_deficit_mass_derivation"]
    eq = data["equivalent_lwe_model_vector_for_aligned_rerun"]

    assert vec["vector_kind"] == "surface_mass_density_kg_m2"
    assert eq["vector_kind"] == "equivalent_lwe_m"
    assert vec["vector_length"] == baseline["baseline_vector"]["length"]
    assert eq["vector_length"] == baseline["baseline_vector"]["length"]
    assert vec["nonzero_entry_count"] > 0
    assert eq["nonzero_entry_count"] > 0

    check_vector_sha(vec, "vector_sha256")
    check_vector_sha(eq, "vector_sha256")

    assert all(data["acceptance_predicates"].values())

    for token in REQUIRED_BOUNDARY:
        assert token in data["physical_interpretation_boundary"] or token in data["forbidden_overclaim_boundary"] or token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT"
    assert data["weakest_sufficient_next_input"] == "NonNullModelComparisonRunOutput"

    print("NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "vector_length": vec["vector_length"],
        "nonzero_entry_count": vec["nonzero_entry_count"],
        "surface_mass_density_sha256": vec["vector_sha256"],
        "equivalent_lwe_sha256": eq["vector_sha256"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
