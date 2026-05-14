from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FiberLargeFromNonPropCore.lean").read_text()
root = Path("lean/Chronos.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/lake_native_fiber_large_from_nonprop_core_2026_05_14.json").read_text())
status = Path("docs/status/CHRONOS_LAKE_NATIVE_FIBER_LARGE_FROM_NONPROP_CORE_2026_05_14.md").read_text()

required_lean = [
    "structure CarrierData",
    "structure FiberWitness",
    "structure NonPropFinalCarrierInvariant",
    "def FiberLargeExistsFromNonProp",
    "theorem fiberLargeExists_from_nonprop_invariant",
    "I.rank_positive c",
    "I.fiber_large_from_rank c",
    "I.entropy_mass_lower c",
    "LAKE_NATIVE_FIBER_LARGE_FROM_NONPROP_CORE_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert "import Chronos.Frontier.FiberLargeFromNonPropCore" in root
assert artifact["status"] == "LAKE_NATIVE_FIBER_LARGE_FROM_NONPROP_CORE_CLOSED"
assert artifact["core_theorem_closed"] is True
assert artifact["downstream_theorem_closure"] is False

required_boundary = [
    "Lake-native core theorem only.",
    "Does not migrate the root `Chronos/Frontier` tree.",
    "Does not prove `UniversalFiberEntropyGap`.",
    "Does not prove Chronos-RR closure.",
    "Does not prove H4.1/FGL closure.",
    "Does not prove P vs NP closure.",
    "Does not prove any Clay-problem closure.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("Lake-native FiberLargeFromNonPropCore verified.")
