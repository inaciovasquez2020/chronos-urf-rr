from pathlib import Path
import json

LEAN = Path("lean/Chronos/Frontier/R1NativeCoherenceRefutation.lean")
ART = Path("artifacts/chronos/r1_native_coherence_refutation_2026_05_24.json")
DOC = Path("docs/status/R1_NATIVE_COHERENCE_REFUTATION_2026_05_24.md")

def main() -> None:
    lean = LEAN.read_text()
    art = json.loads(ART.read_text())
    doc = DOC.read_text()

    required_lean = [
        "import Chronos.Frontier.R1NativeCoherencePromotionTarget",
        "theorem RepositoryNativeR1LongChordCoherence_refuted",
        "¬ RepositoryNativeR1LongChordCoherence",
        "R1UnrestrictedNativeLongChordExclusionFalse",
        "R1CoherentLongChordExclusionProofTarget_proved h",
        "theorem R1NativeCoherenceCounterexampleTarget_proved",
        "R1NativeCoherenceCounterexampleTarget",
        "R1NativeCoherenceRefutationStatus",
        "REPOSITORY_NATIVE_R1_LONG_CHORD_COHERENCE_REFUTED"
    ]

    for token in required_lean:
        assert token in lean, token

    assert art["status"] == "REPOSITORY_NATIVE_R1_LONG_CHORD_COHERENCE_REFUTED"
    assert "RepositoryNativeR1LongChordCoherence_refuted" in art["proved_theorems"]
    assert "R1NativeCoherenceCounterexampleTarget_proved" in art["proved_theorems"]

    required_boundary = [
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

    forbidden_positive_claims = [
        "theorem RepositoryNativeR1LongChordCoherence_proved",
        "theorem NativeAdmissibility_implies_R1LongChordCoherence",
        "axiom NativeAdmissibility_implies_R1LongChordCoherence",
        "theorem NoRepositoryNativeLongChordWitness_proved",
        "theorem Chronos_RR",
        "theorem H4_1_FGL",
        "theorem P_ne_NP"
    ]

    for token in forbidden_positive_claims:
        assert token not in lean, token

    print("R1 native coherence refutation verifier OK")

if __name__ == "__main__":
    main()
