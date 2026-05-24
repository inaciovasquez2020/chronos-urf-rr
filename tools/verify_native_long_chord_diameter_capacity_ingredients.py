#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/native_long_chord_diameter_capacity_ingredients_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/NativeLongChordDiameterCapacityIngredients.lean")
DOC = Path("docs/status/NATIVE_LONG_CHORD_DIAMETER_CAPACITY_INGREDIENTS_2026_05_24.md")
ROOT = Path("lean/Chronos.lean")

REQUIRED_LEAN = [
    "structure LongChordEndpoint",
    "structure LongChordMetricDatum",
    "structure LongChordNativeObject",
    "def LongChordWitness",
    "def NativeLongChordCoherence",
    "theorem long_chord_witness_contradiction",
    "structure DiameterFillingNativeObject",
    "def DiameterFillingCompatibility",
    "theorem monotone_separation_lower_bound",
    "structure LocalTypeCapacityNativeObject",
    "def ExplicitLocalTypeCapacityC",
    "def WithinExplicitLocalTypeCapacity",
    "theorem local_type_capacity_bound_certificate"
]

REQUIRED_BOUNDARY = [
    "R1PromotionProofTarget",
    "R2PromotionProofTarget",
    "R3PromotionProofTarget",
    "NonFactorisationBridgeProofTarget",
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
    lean_text = LEAN.read_text()
    art_text = ART.read_text()
    doc_text = DOC.read_text()
    root_text = ROOT.read_text()

    assert data["status"] == "STRUCTURAL_INGREDIENT_PACKET_CLOSED_PROMOTION_FRONTIER_OPEN"
    assert data["explicit_capacity_bound_C"] == 4096
    assert "import Chronos.Frontier.NativeLongChordDiameterCapacityIngredients" in root_text

    for token in REQUIRED_LEAN:
        assert token in lean_text, token

    for token in data["closed_structural_ingredients"]:
        assert token in lean_text, token
        assert token in art_text, token

    for token in REQUIRED_BOUNDARY:
        assert token in art_text, token
        assert token in doc_text, token

    for token in [
        "R1PromotionProofObstructionEliminationCertificate",
        "R2PromotionProofObstructionEliminationCertificate",
        "R3PromotionProofObstructionEliminationCertificate",
        "NonFactorisationBridgeProofObstructionEliminationCertificate"
    ]:
        assert token in art_text, token
        assert token in doc_text, token

    print("NATIVE_LONG_CHORD_DIAMETER_CAPACITY_INGREDIENTS_OK")

if __name__ == "__main__":
    main()
