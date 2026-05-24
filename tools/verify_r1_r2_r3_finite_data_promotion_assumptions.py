#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/R1R2R3FiniteDataPromotionAssumptions.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
ART = ROOT / "artifacts/chronos/r1_r2_r3_finite_data_promotion_assumptions_2026_05_24.json"
DOC = ROOT / "docs/status/R1_R2_R3_FINITE_DATA_PROMOTION_ASSUMPTIONS_2026_05_24.md"

TOKENS = [
    "def R1FiniteDataToGeneralProofPromotionAssumption : Prop :=",
    "def R2FiniteDataToGeneralProofPromotionAssumption : Prop :=",
    "def R3FiniteDataToGeneralProofPromotionAssumption : Prop :=",
    "theorem repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions",
    "def NonFactorisationConditionalOnRepositoryNativeR1R2R3Instance : Prop :=",
    "theorem non_factorisation_from_finite_data_promotion_assumptions_conditional",
    "def R1R2R3PromotionAssumptionsToNonFactorisationConditionalSurface : Prop :=",
    "theorem r1_r2_r3_promotion_assumptions_to_non_factorisation_conditional_surface"
]

BOUNDARY = [
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
    "UniformLocalTypeCapacity",
    "native R1/R2/R3 instance unconditionally",
    "NON_FACTORISATION unconditionally",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]

def require(cond, msg):
    if not cond:
        raise AssertionError(msg)

def main():
    for path in [LEAN, ROOT_IMPORT, ART, DOC]:
        require(path.exists(), f"missing {path}")

    lean = LEAN.read_text()
    for token in TOKENS:
        require(token in lean, f"missing Lean token: {token}")

    require("import Chronos.Frontier.R1R2R3FiniteDataPromotionAssumptions" in ROOT_IMPORT.read_text(),
            "missing root import")

    data = json.loads(ART.read_text())
    require(data["status"] == "PROMOTION_ASSUMPTION_LAYER_ONLY_NON_FACTORISATION_CONDITIONAL", "wrong status")
    require(data["assembled_conditional_instance"] == "repository_native_r1_r2_r3_instance_from_finite_data_promotion_assumptions", "wrong assembled instance")
    require(data["non_factorisation_surface"] == "non_factorisation_from_finite_data_promotion_assumptions_conditional", "wrong NF surface")

    doc = DOC.read_text()
    for token in BOUNDARY:
        require(token in data["does_not_prove"], f"missing artifact boundary: {token}")
        require(token in doc, f"missing doc boundary: {token}")

    print("R1_R2_R3_FINITE_DATA_PROMOTION_ASSUMPTIONS_OK")

if __name__ == "__main__":
    main()
