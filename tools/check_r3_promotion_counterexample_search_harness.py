#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/r3_promotion_proof_obstruction_certificate_2026_05_24.json")

def main() -> None:
    data = json.loads(ART.read_text())
    assert data["selected_target"] == "R3PromotionProofTarget"
    assert data["counterexample_search_harness"] == "R3PromotionCounterexampleSearchHarnessTarget"
    assert data["target_state"] == "OPEN"
    print("R3_PROMOTION_COUNTEREXAMPLE_SEARCH_HARNESS_TARGET_OK")

if __name__ == "__main__":
    main()
