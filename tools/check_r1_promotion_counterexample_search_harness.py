#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/chronos/r1_promotion_proof_obstruction_certificate_2026_05_24.json"

def fail(msg: str) -> None:
    raise SystemExit(f"R1_PROMOTION_COUNTEREXAMPLE_SEARCH_HARNESS_FAILED: {msg}")

def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)

def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.is_absolute():
        path = ROOT / path

    data = json.loads(path.read_text())

    require(data["artifact"] == "R1_PROMOTION_PROOF_OBSTRUCTION_CERTIFICATE", "wrong artifact")
    require(data["status"] == "R1_SELECTED_OBSTRUCTION_CERTIFICATE_OPEN", "wrong status")
    require(data["selected_target"] == "R1PromotionProofTarget", "wrong selected target")
    require(data["target_status"] == "OPEN", "target must remain OPEN")
    require(data["obstruction_certificate"] == "R1PromotionProofObstructionCertificate", "wrong obstruction certificate")
    require(data["counterexample_search_harness_target"] == "R1PromotionCounterexampleSearchHarnessTarget", "wrong harness target")
    require(data["obstruction_elimination_certificate"] == "R1PromotionProofObstructionEliminationCertificate", "wrong elimination certificate")
    require(data["theorem_target_reduction"] == "R1PromotionProofTargetReductionFromObstructionElimination", "wrong reduction")

    for token in [
        "R1PromotionProofTarget",
        "R1PromotionProofObstructionEliminationCertificate",
        "R1PromotionProofTargetReductionFromObstructionElimination",
        "LongChordExclusion",
        "NON_FACTORISATION unconditionally",
        "P vs NP",
        "any Clay problem"
    ]:
        require(token in data["does_not_prove"], f"missing boundary token: {token}")

    print("R1_PROMOTION_COUNTEREXAMPLE_SEARCH_HARNESS_TARGET_OK")

if __name__ == "__main__":
    main()
