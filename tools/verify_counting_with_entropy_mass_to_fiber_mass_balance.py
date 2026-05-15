from pathlib import Path
import json

lean_path = Path("lean/Chronos/Frontier/CountingWithEntropyMassToFiberMassBalance.lean")
chronos_path = Path("lean/Chronos.lean")
status_path = Path("docs/status/COUNTING_WITH_ENTROPY_MASS_TO_FIBER_MASS_BALANCE_2026_05_15.md")
artifact_path = Path("artifacts/chronos/counting_with_entropy_mass_to_fiber_mass_balance_2026_05_15.json")

lean = lean_path.read_text()
chronos = chronos_path.read_text()
status = status_path.read_text()
artifact_text = artifact_path.read_text()
artifact = json.loads(artifact_text)

required_lean = [
    "def CountingFiberSeparationWithEntropyMassFromNonProp",
    "W.fiber.entropyMass = I.entropyMass c",
    "theorem countingFiberSeparation_from_counting_with_entropy_mass",
    "theorem fiberMassBalance_from_counting_with_entropy_mass",
    "theorem universalFiberEntropyGap_from_counting_with_entropy_mass",
    "FiberMassBalanceFromNonProp I",
    "UniversalFiberEntropyGapFromNonProp I",
    "Conditional enriched-counting bridge only",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.CountingWithEntropyMassToFiberMassBalance" in chronos

assert artifact["status"] == "ENRICHED_COUNTING_TO_MASS_BRIDGE_CLOSED"
assert artifact["new_predicate"] == "CountingFiberSeparationWithEntropyMassFromNonProp"
assert artifact["added_datum"] == "W.fiber.entropyMass = I.entropyMass c"

required_status = [
    "This proves only the enriched-counting bridge.",
    "It does not prove:",
    "FiberMassBalance from ordinary CountingFiberSeparationFromNonProp alone",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

required_nonclaims = {
    "FiberMassBalance from ordinary CountingFiberSeparationFromNonProp alone",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

assert required_nonclaims.issubset(set(artifact["does_not_prove"]))

forbidden = [
    "FiberMassBalance from ordinary CountingFiberSeparationFromNonProp alone is proved",
    "ordinary CountingFiberSeparationFromNonProp alone proves FiberMassBalance",
    "unrestricted UniversalFiberEntropyGap is proved",
    "unrestricted Chronos-RR is proved",
    "H4.1/FGL is proved",
    "P vs NP is solved",
    "Clay problem is solved",
]

combined = lean + "\n" + status + "\n" + artifact_text

for token in forbidden:
    assert token.lower() not in combined.lower(), token

print("Counting-with-entropy-mass to FiberMassBalance bridge verified.")
