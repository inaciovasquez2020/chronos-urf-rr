#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/r1_r2_r3_promotion_obstruction_frontier_lock_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R1R2R3PromotionObstructionFrontierLock.lean")
DOC = Path("docs/status/R1_R2_R3_PROMOTION_OBSTRUCTION_FRONTIER_LOCK_2026_05_24.md")

REQUIRED = [
    "R1PromotionProofObstructionCertificate",
    "R2PromotionProofObstructionCertificate",
    "R3PromotionProofObstructionCertificate",
    "NonFactorisationBridgeProofObstructionCertificate",
    "R1PromotionProofObstructionEliminationCertificate",
    "R2PromotionProofObstructionEliminationCertificate",
    "R3PromotionProofObstructionEliminationCertificate",
    "NonFactorisationBridgeProofObstructionEliminationCertificate",
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

    assert data["status"] == "PROMOTION_OBSTRUCTION_FRONTIER_LOCKED_OPEN"
    assert data["frontier_state"] == "OPEN"
    assert len(data["recorded_obstruction_certificates"]) == 4
    assert len(data["closure_requires"]) == 4

    for token in REQUIRED:
        assert token in art_text, token
        assert token in doc_text, token
    for token in REQUIRED[:8]:
        assert token in lean_text, token

    print("R1_R2_R3_PROMOTION_OBSTRUCTION_FRONTIER_LOCK_OK")

if __name__ == "__main__":
    main()
