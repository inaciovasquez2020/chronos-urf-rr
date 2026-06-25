#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/external_validation/represents_terminal_semantic_payload_source_location_2026_06_24.json"
DOC = ROOT / "docs/status/REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["target"] == "REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION"
    assert data["status"] == "candidate_located_not_realized"

    literal = data["literal_relation_search"]
    for key in ["represents_terminal", "RepresentsTerminal", "representsTerminal"]:
        assert literal[key] == "absent_from_non_status_source_tree"

    required_locations = {
        ("lean/Chronos/Frontier/R1R2R3SemanticTheoremProofTargets.lean", "R1SemanticData"),
        ("lean/Chronos/Frontier/R1ConcreteSemanticDataInstance.lean", "R1ConcreteNativeSafeSemanticData"),
        ("lean/Chronos/Frontier/TerminalAdmissibleBoundaryChainCertificate.lean", "TerminalAdmissibleBoundaryChainCertificate"),
    }

    actual_locations = {
        (item["file"], item["object"])
        for item in data["candidate_source_locations"]
    }

    assert required_locations <= actual_locations

    for file_name, object_name in required_locations:
        assert file_name in doc
        assert object_name in doc

    for token in [
        "BOUNDARY := not represents_terminal_definition_found",
        "BOUNDARY := not REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_realized",
        "BOUNDARY := not REPRESENTS_TERMINAL_DISCHARGE_SEMANTICS_FIELD_REALIZATION_proved",
        "BOUNDARY := not DISCHARGE_TRANSFER_SEMANTIC_INVARIANCE_proved_nonconditionally",
        "BOUNDARY := not unrestricted_terminal_closure_proved_nonconditionally",
        "BOUNDARY := not final_closure_claim_proved",
    ]:
        assert token in data["boundary"]
        assert token in doc

    print("REPRESENTS_TERMINAL_SEMANTIC_PAYLOAD_SOURCE_LOCATION_2026_06_24_OK")

if __name__ == "__main__":
    main()
