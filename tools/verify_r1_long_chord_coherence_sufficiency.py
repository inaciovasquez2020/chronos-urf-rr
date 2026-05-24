#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/r1_long_chord_coherence_sufficiency_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R1LongChordCoherenceSufficiency.lean")
DOC = Path("docs/status/R1_LONG_CHORD_COHERENCE_SUFFICIENCY_2026_05_24.md")
ROOT = Path("lean/Chronos.lean")

REQUIRED_LEAN = [
    "def RepositoryNativeR1LongChordCoherence",
    "def NoRepositoryNativeLongChordWitness",
    "theorem repository_native_r1_long_chord_coherence_blocks_witness",
    "def R1LongChordCoherenceToPromotionObstructionEliminationTarget",
    "def R1LongChordCoherenceSufficiencyFrontierOpen"
]

BOUNDARY = [
    "R1PromotionProofObstructionEliminationCertificate",
    "R1PromotionProofTarget",
    "LongChordExclusion",
    "DiameterSeparationFillingObstruction",
    "UniformLocalTypeCapacity",
    "NonFactorisationBridgeProofTarget",
    "NON_FACTORISATION unconditionally",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]

def main() -> None:
    data = json.loads(ART.read_text())
    lean_text = LEAN.read_text()
    art_text = ART.read_text()
    doc_text = DOC.read_text()
    root_text = ROOT.read_text()

    assert data["status"] == "R1_COHERENCE_WITNESS_EXCLUSION_CLOSED_PROMOTION_ELIMINATION_OPEN"
    assert "import Chronos.Frontier.R1LongChordCoherenceSufficiency" in root_text

    for token in REQUIRED_LEAN:
        assert token in lean_text, token
        assert token in art_text, token

    assert "long_chord_witness_contradiction" in lean_text
    assert "R1LongChordCoherenceToPromotionObstructionEliminationTarget proof" in art_text
    assert "R1PromotionProofObstructionEliminationCertificate" in art_text

    for token in BOUNDARY:
        assert token in art_text, token
        assert token in doc_text, token

    print("R1_LONG_CHORD_COHERENCE_SUFFICIENCY_OK")

if __name__ == "__main__":
    main()
