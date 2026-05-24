#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/non_factorisation_bridge_proof_obstruction_certificate_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/NonFactorisationBridgeProofObstructionCertificate.lean")
DOC = Path("docs/status/NON_FACTORISATION_BRIDGE_PROOF_OBSTRUCTION_CERTIFICATE_2026_05_24.md")

REQUIRED_JSON = [
    "NonFactorisationBridgeProofTarget",
    "NonFactorisationBridgeProofObstructionCertificate",
    "NonFactorisationBridgeCounterexampleSearchHarnessTarget",
    "NonFactorisationBridgeProofObstructionEliminationCertificate",
    "NonFactorisationBridgeProofTargetReductionFromObstructionElimination",
    "OPEN"
]

REQUIRED_LEAN = [
    "def NonFactorisationBridgeProofObstructionCertificate",
    "theorem non_factorisation_bridge_proof_obstruction_certificate",
    "def NonFactorisationBridgeCounterexampleSearchHarnessTarget",
    "theorem non_factorisation_bridge_counterexample_search_harness_target",
    "def NonFactorisationBridgeProofObstructionEliminationCertificate",
    "def NonFactorisationBridgeProofTargetReductionFromObstructionElimination",
    "theorem non_factorisation_bridge_proof_target_reduction_from_obstruction_elimination"
]

BOUNDARY = [
    "NonFactorisationBridgeProofTarget",
    "R1PromotionProofTarget",
    "R2PromotionProofTarget",
    "R3PromotionProofTarget",
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
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

    assert data["status"] == "NON_FACTORISATION_BRIDGE_PROOF_OBSTRUCTION_CERTIFICATE_OPEN_FRONTIER"
    for token in REQUIRED_JSON:
        assert token in art_text, token
    for token in REQUIRED_LEAN:
        assert token in lean_text, token
    for token in BOUNDARY:
        assert token in art_text, token
        assert token in doc_text, token

    print("NON_FACTORISATION_BRIDGE_PROOF_OBSTRUCTION_CERTIFICATE_OK")

if __name__ == "__main__":
    main()
