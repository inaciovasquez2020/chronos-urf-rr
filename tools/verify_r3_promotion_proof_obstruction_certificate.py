#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/r3_promotion_proof_obstruction_certificate_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R3PromotionProofObstructionCertificate.lean")
DOC = Path("docs/status/R3_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_2026_05_24.md")

REQUIRED_JSON = [
    "R3PromotionProofTarget",
    "R3PromotionProofObstructionCertificate",
    "R3PromotionCounterexampleSearchHarnessTarget",
    "R3PromotionProofObstructionEliminationCertificate",
    "R3PromotionProofTargetReductionFromObstructionElimination",
    "OPEN"
]

REQUIRED_LEAN = [
    "def R3PromotionProofObstructionCertificate",
    "theorem r3_promotion_proof_obstruction_certificate",
    "def R3PromotionCounterexampleSearchHarnessTarget",
    "theorem r3_promotion_counterexample_search_harness_target",
    "def R3PromotionProofObstructionEliminationCertificate",
    "def R3PromotionProofTargetReductionFromObstructionElimination",
    "theorem r3_promotion_proof_target_reduction_from_obstruction_elimination"
]

BOUNDARY = [
    "R3PromotionProofTarget",
    "UniformLocalTypeCapacity",
    "NON_FACTORISATION unconditionally",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]

def main() -> None:
    data = json.loads(ART.read_text())
    art_text = ART.read_text()
    lean_text = LEAN.read_text()
    doc_text = DOC.read_text()

    assert data["status"] == "R3_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_OPEN_FRONTIER"
    for token in REQUIRED_JSON:
        assert token in art_text, token
    for token in REQUIRED_LEAN:
        assert token in lean_text, token
    for token in BOUNDARY:
        assert token in art_text, token
        assert token in doc_text, token

    print("R3_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE_OK")

if __name__ == "__main__":
    main()
