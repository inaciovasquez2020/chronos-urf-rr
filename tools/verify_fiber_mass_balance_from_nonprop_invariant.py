from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FiberMassBalanceFromNonPropInvariant.lean").read_text()
root = Path("lean/Chronos.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/fiber_mass_balance_from_nonprop_invariant_2026_05_14.json").read_text())
status = Path("docs/status/CHRONOS_FIBER_MASS_BALANCE_FROM_NONPROP_INVARIANT_2026_05_14.md").read_text()

required_lean = [
    "structure FiberMassBalanceWitness",
    "def FiberMassBalanceFromNonProp",
    "theorem fiberMassBalance_from_nonprop_invariant",
    "theorem countingFiberSeparation_and_fiberMassBalance_from_nonprop_invariant",
    "I.rank_positive c",
    "I.entropy_mass_lower c",
    "countingFiberSeparation_from_nonprop_invariant I",
    "LAKE_NATIVE_FIBER_MASS_BALANCE_FROM_NONPROP_INVARIANT_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert "import Chronos.Frontier.FiberMassBalanceFromNonPropInvariant" in root
assert artifact["status"] == "LAKE_NATIVE_FIBER_MASS_BALANCE_FROM_NONPROP_INVARIANT_CLOSED"
assert artifact["core_theorem_closed"] is True
assert artifact["downstream_theorem_closure"] is False

required_boundary = [
    "Lake-native fiber-mass-balance theorem only.",
    "Does not prove UniversalFiberEntropyGap.",
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

print("FiberMassBalanceFromNonPropInvariant verified.")
