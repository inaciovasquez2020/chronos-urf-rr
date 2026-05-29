#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel.lean"
ART = ROOT / "artifacts/sparc/concrete_predictive_deficit_mass_law_or_concrete_low_parameter_deficit_mass_model_2026_05_28.json"
DOC = ROOT / "docs/status/CONCRETE_PREDICTIVE_DEFICIT_MASS_LAW_OR_CONCRETE_LOW_PARAMETER_DEFICIT_MASS_MODEL_2026_05_28.md"
CHRONOS = ROOT / "lean/Chronos.lean"

for path in [LEAN, ART, DOC, CHRONOS]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = LEAN.read_text()
doc_text = DOC.read_text()
chronos_text = CHRONOS.read_text()
artifact = json.loads(ART.read_text())

required_lean_tokens = [
    "ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel",
    "concreteDeficitMassParameterVector",
    "concreteLowParameterDeficitMassModelTarget",
    "concreteLowParameterDeficitMassModelTarget_admissible",
    "concretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModelV1",
    "concreteModelV1_projects_to_admissible_target",
    "concreteModelV1_is_low_parameter_route",
    "concreteModelV1_parameter_count_within_bound",
    "concreteModelV1_has_no_empirical_validation_claim",
    "concreteModelV1_has_no_physical_replacement_claim",
]

required_doc_tokens = [
    "CONCRETE_CANDIDATE_ONLY_NO_EMPIRICAL_VALIDATION",
    "Does not prove: predictive GDM law closure.",
    "Does not prove: low-parameter deficit-mass model closure.",
    "Does not prove: dark matter replacement claim.",
    "Does not prove: Lambda-CDM failure claim.",
    "Does not prove: physical validation claim.",
    "Does not prove: independent holdout validation claim.",
    "Does not prove: SPARC empirical victory claim.",
    "Does not prove: PhD-complete final result claim.",
    "Does not prove: unrestricted Chronos-RR.",
    "Does not prove: unrestricted H4.1/FGL.",
    "Does not prove: P vs NP.",
    "Does not prove: Clay problem.",
    "IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel",
]

required_artifact = {
    "id": "CONCRETE_PREDICTIVE_DEFICIT_MASS_LAW_OR_CONCRETE_LOW_PARAMETER_DEFICIT_MASS_MODEL_2026_05_28",
    "status": "CONCRETE_CANDIDATE_ONLY_NO_EMPIRICAL_VALIDATION",
    "object_name": "ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel",
    "next_missing_object": "IndependentHoldoutValidationRunForConcretePredictiveDeficitMassModel",
    "parameter_count": 2,
    "low_parameter_bound": 8,
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

if artifact.get("parameter_vector") != [0, 1]:
    raise SystemExit("unexpected parameter_vector")

for boundary in [
    "predictive GDM law closure",
    "low-parameter deficit-mass model closure",
    "dark matter replacement claim",
    "Lambda-CDM failure claim",
    "physical validation claim",
    "independent holdout validation claim",
    "SPARC empirical victory claim",
    "PhD-complete final result claim",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]:
    if boundary not in artifact.get("does_not_prove", []):
        raise SystemExit(f"missing artifact boundary: {boundary}")

import_line = "import Chronos.Frontier.ConcretePredictiveDeficitMassLawOrConcreteLowParameterDeficitMassModel"
if import_line not in chronos_text:
    raise SystemExit(f"missing Chronos import: {import_line}")

if "import Chronos.Frontier.PredictiveDeficitMassLawOrLowParameterDeficitMassModel" not in lean_text:
    raise SystemExit("missing dependency import in concrete Lean module")

print("CONCRETE_PREDICTIVE_DEFICIT_MASS_LAW_OR_CONCRETE_LOW_PARAMETER_DEFICIT_MASS_MODEL_OK")
