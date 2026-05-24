from pathlib import Path
import json

LEAN = Path("lean/Chronos/Frontier/R1NativeCoherencePromotionTarget.lean")
ART = Path("artifacts/chronos/r1_native_coherence_promotion_target_2026_05_24.json")
DOC = Path("docs/status/R1_NATIVE_COHERENCE_PROMOTION_TARGET_2026_05_24.md")

def main() -> None:
    lean = LEAN.read_text()
    art = json.loads(ART.read_text())
    doc = DOC.read_text()

    required_lean = [
        "import Chronos.Frontier.R1NativeCounterexampleCoherentRestriction",
        "def NativeAdmissibilityPackage : Prop",
        "def R1NativeCoherencePromotionTarget : Prop",
        "NativeAdmissibilityPackage → RepositoryNativeR1LongChordCoherence",
        "def R1NativeCoherenceCounterexampleTarget : Prop",
        "NativeAdmissibilityPackage ∧ ¬ RepositoryNativeR1LongChordCoherence",
        "def NativeAdmissibility_implies_R1LongChordCoherence_OPEN : Prop",
        "def NativeAdmissibility_R1LongChordCoherence_counterexample_OPEN : Prop",
        "R1_COHERENCE_PROMOTION_TARGET_OPEN_ONLY"
    ]

    for token in required_lean:
        assert token in lean, token

    assert art["status"] == "OPEN_PROMOTION_TARGET_ONLY"
    assert art["open_problem"] == "NativeAdmissibilityPackage -> RepositoryNativeR1LongChordCoherence"
    assert art["counterexample_target"] == "NativeAdmissibilityPackage and not RepositoryNativeR1LongChordCoherence"

    required_boundary = [
        "does not prove NativeAdmissibilityPackage -> RepositoryNativeR1LongChordCoherence",
        "does not prove RepositoryNativeR1LongChordCoherence",
        "does not prove NoRepositoryNativeLongChordWitness",
        "does not prove opaque LongChordExclusionProofTarget",
        "does not prove theorem-level R1 promotion",
        "does not prove R2",
        "does not prove R3",
        "does not prove NON_FACTORISATION",
        "does not prove Chronos-RR",
        "does not prove H4.1/FGL",
        "does not prove P vs NP",
        "does not prove any Clay problem"
    ]

    for token in required_boundary:
        assert token in doc, token
        assert token in art["boundary"], token

    forbidden_promotions = [
        "theorem NativeAdmissibility_implies_R1LongChordCoherence",
        "axiom NativeAdmissibility_implies_R1LongChordCoherence",
        "theorem RepositoryNativeR1LongChordCoherence_from_native_admissibility",
        "theorem Chronos_RR",
        "theorem H4_1_FGL",
        "theorem P_ne_NP"
    ]

    for token in forbidden_promotions:
        assert token not in lean, token

    print("R1 native coherence promotion target verifier OK")

if __name__ == "__main__":
    main()
