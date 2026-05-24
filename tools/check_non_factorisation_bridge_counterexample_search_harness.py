#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/non_factorisation_bridge_proof_obstruction_certificate_2026_05_24.json")

def main() -> None:
    data = json.loads(ART.read_text())
    assert data["selected_target"] == "NonFactorisationBridgeProofTarget"
    assert data["counterexample_search_harness"] == "NonFactorisationBridgeCounterexampleSearchHarnessTarget"
    assert data["target_state"] == "OPEN"
    assert "NON_FACTORISATION_BRIDGE_COUNTEREXAMPLE_SEARCH_RESULT" in data["next_missing_objects"]
    print("NON_FACTORISATION_BRIDGE_COUNTEREXAMPLE_SEARCH_HARNESS_TARGET_OK")

if __name__ == "__main__":
    main()
