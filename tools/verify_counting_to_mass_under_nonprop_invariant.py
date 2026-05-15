from pathlib import Path
import json

lean_path = Path("lean/Chronos/Frontier/CountingToMassUnderNonPropInvariant.lean")
chronos_path = Path("lean/Chronos.lean")
status_path = Path("docs/status/COUNTING_TO_MASS_UNDER_NONPROP_INVARIANT_2026_05_15.md")
artifact_path = Path("artifacts/chronos/counting_to_mass_under_nonprop_invariant_2026_05_15.json")

lean = lean_path.read_text()
chronos = chronos_path.read_text()
status = status_path.read_text()
artifact_text = artifact_path.read_text()
artifact = json.loads(artifact_text)

required_lean = [
    "theorem fiberMassBalance_from_countingFiberSeparation_under_nonprop_invariant",
    "(_hcount : CountingFiberSeparationFromNonProp I)",
    "FiberMassBalanceFromNonProp I",
    "exact fiberMassBalance_from_nonprop_invariant I",
    "theorem universalFiberEntropyGap_from_countingFiberSeparation_under_nonprop_invariant",
    "UniversalFiberEntropyGapFromNonProp I",
    "COUNTING_TO_MASS_UNDER_NONPROP_INVARIANT_CLOSED_ONLY",
    "not used to reconstruct entropyMass",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.CountingToMassUnderNonPropInvariant" in chronos

assert artifact["status"] == "TYPED_REPOSITORY_BRIDGE_CLOSED_ONLY"
assert artifact["context"] == "I : NonPropFinalCarrierInvariant"

required_status = [
    "CountingFiberSeparationFromNonProp I",
    "→ FiberMassBalanceFromNonProp I",
    "I : NonPropFinalCarrierInvariant",
    "The counting premise is not used to reconstruct entropyMass.",
    "This proves only the typed repository bridge under NonPropFinalCarrierInvariant.",
    "standalone CountingFiberSeparationToFiberMassBalance",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

required_nonclaims = {
    "standalone CountingFiberSeparationToFiberMassBalance",
    "entropyMass reconstruction from ordinary CountingFiberSeparationFromNonProp alone",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

assert required_nonclaims.issubset(set(artifact["does_not_prove"]))

forbidden = [
    "standalone CountingFiberSeparationToFiberMassBalance is proved",
    "entropyMass reconstruction from ordinary CountingFiberSeparationFromNonProp alone is proved",
    "ordinary CountingFiberSeparationFromNonProp alone reconstructs entropyMass",
    "unrestricted UniversalFiberEntropyGap is proved",
    "unrestricted Chronos-RR is proved",
    "H4.1/FGL is proved",
    "P vs NP is solved",
    "Clay problem is solved",
]

combined = lean + "\n" + status + "\n" + artifact_text

for token in forbidden:
    assert token.lower() not in combined.lower(), token

print("Counting-to-mass under NonProp invariant bridge verified.")
