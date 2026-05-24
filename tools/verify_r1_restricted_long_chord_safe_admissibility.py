from pathlib import Path
import json

LEAN = Path("lean/Chronos/Frontier/R1RestrictedLongChordSafeAdmissibility.lean")
ART = Path("artifacts/chronos/r1_restricted_long_chord_safe_admissibility_2026_05_24.json")
DOC = Path("docs/status/R1_RESTRICTED_LONG_CHORD_SAFE_ADMISSIBILITY_2026_05_24.md")

def main() -> None:
    lean = LEAN.read_text()
    art = json.loads(ART.read_text())
    doc = DOC.read_text()

    required_lean = [
        "import Chronos.Frontier.R1NativeCoherenceRefutation",
        "def R1LongChordSafeNativeAdmissible",
        "¬ LongChordWitness x",
        "def R1RestrictedNoLongChordWitness",
        "theorem R1RestrictedNoLongChordWitness_proved",
        "theorem R1NativeLongChordCounterexampleObject_not_safe",
        "R1NativeLongChordCounterexampleObject_is_witness",
        "R1RestrictedLongChordSafeAdmissibilityStatus",
        "RESTRICTED_R1_LONG_CHORD_SAFE_ADMISSIBILITY_CLOSED"
    ]

    for token in required_lean:
        assert token in lean, token

    assert art["status"] == "RESTRICTED_R1_LONG_CHORD_SAFE_ADMISSIBILITY_CLOSED"
    assert "R1RestrictedNoLongChordWitness_proved" in art["proved_theorems"]
    assert "R1NativeLongChordCounterexampleObject_not_safe" in art["proved_theorems"]

    required_boundary = [
        "does not prove RepositoryNativeR1LongChordCoherence",
        "does not prove NoRepositoryNativeLongChordWitness",
        "does not prove opaque LongChordExclusionProofTarget",
        "does not prove theorem-level unrestricted R1 promotion",
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
        "theorem NoRepositoryNativeLongChordWitness_proved",
        "theorem LongChordExclusionProofTarget_proved",
        "theorem Chronos_RR",
        "theorem H4_1_FGL",
        "theorem P_ne_NP"
    ]

    for token in forbidden_positive_claims:
        assert token not in lean, token

    print("R1 restricted long-chord-safe admissibility verifier OK")

if __name__ == "__main__":
    main()
