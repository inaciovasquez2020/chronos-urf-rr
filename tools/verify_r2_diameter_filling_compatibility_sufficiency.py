#!/usr/bin/env python3
from pathlib import Path
import json

ART = Path("artifacts/chronos/r2_diameter_filling_compatibility_sufficiency_2026_05_24.json")
LEAN = Path("lean/Chronos/Frontier/R2DiameterFillingCompatibilitySufficiency.lean")
DOC = Path("docs/status/R2_DIAMETER_FILLING_COMPATIBILITY_SUFFICIENCY_2026_05_24.md")
ROOT = Path("lean/Chronos.lean")

REQUIRED_LEAN = [
    "def RepositoryNativeR2DiameterFillingCompatibility",
    "def RepositoryNativeR2SeparationLowerBound",
    "theorem repository_native_r2_diameter_filling_compatibility_gives_lower_bound",
    "def R2DiameterFillingCompatibilityToPromotionObstructionEliminationTarget",
    "def R2DiameterFillingCompatibilitySufficiencyFrontierOpen"
]

BOUNDARY = [
    "R2PromotionProofObstructionEliminationCertificate",
    "R2PromotionProofTarget",
    "DiameterSeparationFillingObstruction",
    "R1PromotionProofObstructionEliminationCertificate",
    "R3PromotionProofObstructionEliminationCertificate",
    "NonFactorisationBridgeProofTarget",
    "LongChordExclusion",
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

    assert data["status"] == "R2_COMPATIBILITY_LOWER_BOUND_CLOSED_PROMOTION_ELIMINATION_OPEN"
    assert "import Chronos.Frontier.R2DiameterFillingCompatibilitySufficiency" in root_text

    for token in REQUIRED_LEAN:
        assert token in lean_text, token

    for token in data["closed_structural_ingredients"]:
        assert token in lean_text, token
        assert token in art_text, token

    assert "monotone_separation_lower_bound" in lean_text
    assert "R2DiameterFillingCompatibilityToPromotionObstructionEliminationTarget proof" in art_text
    assert "R2PromotionProofObstructionEliminationCertificate" in art_text

    for token in BOUNDARY:
        assert token in art_text, token
        assert token in doc_text, token

    print("R2_DIAMETER_FILLING_COMPATIBILITY_SUFFICIENCY_OK")

if __name__ == "__main__":
    main()
