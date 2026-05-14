from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/UniversalFiberEntropyGapFromCountingAndMass.lean").read_text()
root = Path("lean/Chronos.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/universal_fiber_entropy_gap_from_counting_and_mass_2026_05_14.json").read_text())
status = Path("docs/status/CHRONOS_UNIVERSAL_FIBER_ENTROPY_GAP_FROM_COUNTING_AND_MASS_2026_05_14.md").read_text()

required_lean = [
    "structure UniversalFiberEntropyGapWitness",
    "def UniversalFiberEntropyGapFromNonProp",
    "theorem universalFiberEntropyGap_from_counting_and_mass",
    "theorem universalFiberEntropyGap_from_nonprop_invariant",
    "countingFiberSeparation_from_nonprop_invariant I",
    "fiberMassBalance_from_nonprop_invariant I",
    "LAKE_NATIVE_UNIVERSAL_FIBER_ENTROPY_GAP_FROM_COUNTING_AND_MASS_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert "import Chronos.Frontier.UniversalFiberEntropyGapFromCountingAndMass" in root
assert artifact["status"] == "LAKE_NATIVE_UNIVERSAL_FIBER_ENTROPY_GAP_FROM_COUNTING_AND_MASS_CLOSED"
assert artifact["core_theorem_closed"] is True
assert artifact["downstream_theorem_closure"] is False

required_boundary = [
    "Lake-native UniversalFiberEntropyGap assembly only.",
    "Does not prove Chronos-RR closure.",
    "Does not prove H4.1/FGL closure.",
    "Does not prove P vs NP closure.",
    "Does not prove any Clay-problem closure.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("UniversalFiberEntropyGapFromCountingAndMass verified.")
