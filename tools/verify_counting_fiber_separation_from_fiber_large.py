from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/CountingFiberSeparationFromFiberLarge.lean").read_text()
root = Path("lean/Chronos.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/counting_fiber_separation_from_fiber_large_2026_05_14.json").read_text())
status = Path("docs/status/CHRONOS_COUNTING_FIBER_SEPARATION_FROM_FIBER_LARGE_2026_05_14.md").read_text()

required_lean = [
    "structure CountingFiberSeparationWitness",
    "def CountingFiberSeparationFromNonProp",
    "theorem countingFiberSeparation_from_fiberLargeExists",
    "theorem countingFiberSeparation_from_nonprop_invariant",
    "fiberLargeExists_from_nonprop_invariant I",
    "LAKE_NATIVE_COUNTING_FIBER_SEPARATION_FROM_FIBER_LARGE_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert "import Chronos.Frontier.CountingFiberSeparationFromFiberLarge" in root
assert artifact["status"] == "LAKE_NATIVE_COUNTING_FIBER_SEPARATION_FROM_FIBER_LARGE_CLOSED"
assert artifact["core_theorem_closed"] is True
assert artifact["downstream_theorem_closure"] is False

required_boundary = [
    "Lake-native counting-separation theorem only.",
    "Does not prove FiberMassBalance.",
    "Does not prove UniversalFiberEntropyGap.",
    "Does not prove Chronos-RR closure.",
    "Does not prove H4.1/FGL closure.",
    "Does not prove P vs NP closure.",
    "Does not prove any Clay-problem closure.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "FiberMassBalance is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("CountingFiberSeparationFromFiberLarge verified.")
