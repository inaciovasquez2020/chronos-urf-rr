#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/R1PromotionProofObstructionCertificate.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
ART = ROOT / "artifacts/chronos/r1_promotion_proof_obstruction_certificate_2026_05_24.json"
DOC = ROOT / "docs/status/R1_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_2026_05_24.md"
HARNESS = ROOT / "tools/check_r1_promotion_counterexample_search_harness.py"

TOKENS = [
    "def R1PromotionProofObstructionCertificate : Prop := True",
    "def R1PromotionCounterexampleSearchHarnessTarget : Prop :=",
    "def R1PromotionProofObstructionEliminationCertificate : Prop :=",
    "def R1PromotionProofTargetReductionFromObstructionElimination : Prop :=",
    "def R1PromotionSelectedTargetOpen : Prop :=",
    "def R1PromotionSelectedTargetStatus : String := \"OPEN\"",
    "def R1PromotionProofObstructionStatus : String := \"OPEN\""
]

BOUNDARY = [
    "R1PromotionProofTarget",
    "R1PromotionProofObstructionEliminationCertificate",
    "R1PromotionProofTargetReductionFromObstructionElimination",
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
    for path in [LEAN, ROOT_IMPORT, ART, DOC, HARNESS]:
        require(path.exists(), f"missing {path}")

    lean = LEAN.read_text()
    for token in TOKENS:
        require(token in lean, f"missing Lean token: {token}")

    require("import Chronos.Frontier.R1PromotionProofObstructionCertificate" in ROOT_IMPORT.read_text(),
            "missing root import")

    data = json.loads(ART.read_text())
    require(data["status"] == "R1_SELECTED_OBSTRUCTION_CERTIFICATE_OPEN", "wrong status")
    require(data["selected_target"] == "R1PromotionProofTarget", "wrong selected target")
    require(data["target_status"] == "OPEN", "target must remain OPEN")

    doc = DOC.read_text()
    for token in BOUNDARY:
        require(token in data["does_not_prove"], f"missing artifact boundary: {token}")
        require(token in doc, f"missing doc boundary: {token}")

    print("R1_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_OK")

if __name__ == "__main__":
    main()
