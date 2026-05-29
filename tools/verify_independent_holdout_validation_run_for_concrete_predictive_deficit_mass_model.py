#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel.lean"
ART = ROOT / "artifacts/sparc/independent_holdout_validation_run_for_concrete_predictive_deficit_mass_model_2026_05_29.json"
DOC = ROOT / "docs/status/INDEPENDENT_HOLDOUT_VALIDATION_RUN_FOR_CONCRETE_PREDICTIVE_DEFICIT_MASS_MODEL_2026_05_29.md"
CHRONOS = ROOT / "lean/Chronos.lean"

for path in [LEAN, ART, DOC, CHRONOS]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = LEAN.read_text()
doc_text = DOC.read_text()
chronos_text = CHRONOS.read_text()
artifact = json.loads(ART.read_text())

required_lean_tokens = [
    "IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel",
    "HoldoutGalaxyRecord",
    "holdoutResidual",
    "totalHoldoutResidual",
    "concreteIndependentHoldoutRecords",
    "concreteIndependentHoldoutRecords_nonempty",
    "concreteIndependentHoldoutRecords_total_residual_zero",
    "independentHoldoutValidationRunForConcretePredictiveDeficitMassModelV1",
    "independentHoldoutRunV1_projects_to_concrete_model",
    "independentHoldoutRunV1_has_positive_holdout",
    "independentHoldoutRunV1_has_frozen_before_holdout_guard",
    "independentHoldoutRunV1_has_independent_holdout_guard",
    "independentHoldoutRunV1_total_residual_zero",
    "independentHoldoutRunV1_has_no_authentic_sparc_validation_claim",
    "independentHoldoutRunV1_has_no_empirical_victory_claim",
    "independentHoldoutRunV1_has_no_physical_replacement_claim",
]

required_doc_tokens = [
    "FINITE_HOLDOUT_CERTIFICATE_ONLY_NO_AUTHENTIC_EMPIRICAL_VALIDATION",
    "Does not prove: authentic SPARC empirical validation.",
    "Does not prove: independent real-data holdout validation.",
    "Does not prove: predictive GDM law closure.",
    "Does not prove: low-parameter deficit-mass model closure.",
    "Does not prove: dark matter replacement claim.",
    "Does not prove: Lambda-CDM failure claim.",
    "Does not prove: physical validation claim.",
    "Does not prove: SPARC empirical victory claim.",
    "Does not prove: PhD-complete final result claim.",
    "Does not prove: unrestricted Chronos-RR.",
    "Does not prove: unrestricted H4.1/FGL.",
    "Does not prove: P vs NP.",
    "Does not prove: Clay problem.",
    "AuthenticSPARCHoldoutDatasetBindingAndExecution",
]

required_artifact = {
    "id": "INDEPENDENT_HOLDOUT_VALIDATION_RUN_FOR_CONCRETE_PREDICTIVE_DEFICIT_MASS_MODEL_2026_05_29",
    "status": "FINITE_HOLDOUT_CERTIFICATE_ONLY_NO_AUTHENTIC_EMPIRICAL_VALIDATION",
    "object_name": "IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel",
    "model_object": "ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel",
    "holdout_record_count": 2,
    "total_holdout_residual": 0,
    "next_missing_object": "AuthenticSPARCHoldoutDatasetBindingAndExecution",
}

for token in required_lean_tokens:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for token in required_doc_tokens:
    if token not in doc_text:
        raise SystemExit(f"missing doc token: {token}")

for key, expected in required_artifact.items():
    actual = artifact.get(key)
    if actual != expected:
        raise SystemExit(f"artifact mismatch for {key}: expected {expected!r}, got {actual!r}")

guards = artifact.get("guards", {})
expected_guards = {
    "frozen_before_holdout_guard": True,
    "independent_holdout_guard": True,
    "authentic_sparc_validation_claim": False,
    "empirical_victory_claim": False,
    "physical_replacement_claim": False,
}
for key, expected in expected_guards.items():
    actual = guards.get(key)
    if actual != expected:
        raise SystemExit(f"guard mismatch for {key}: expected {expected!r}, got {actual!r}")

for boundary in [
    "authentic SPARC empirical validation",
    "independent real-data holdout validation",
    "predictive GDM law closure",
    "low-parameter deficit-mass model closure",
    "dark matter replacement claim",
    "Lambda-CDM failure claim",
    "physical validation claim",
    "SPARC empirical victory claim",
    "PhD-complete final result claim",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]:
    if boundary not in artifact.get("does_not_prove", []):
        raise SystemExit(f"missing artifact boundary: {boundary}")

import_line = "import Chronos.Frontier.IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel"
if import_line not in chronos_text:
    raise SystemExit(f"missing Chronos import: {import_line}")

dependency_import = "import Chronos.Frontier.ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel"
if dependency_import not in lean_text:
    raise SystemExit("missing dependency import in holdout Lean module")

print("INDEPENDENT_HOLDOUT_VALIDATION_RUN_FOR_CONCRETE_PREDICTIVE_DEFICIT_MASS_MODEL_OK")
