from pathlib import Path
import json

lean = Path("Chronos/Frontier/NonPropFinalCarrierInvariant.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/nonprop_final_carrier_invariant_2026_05_14.json").read_text())
status = Path("docs/status/CHRONOS_NONPROP_FINAL_CARRIER_INVARIANT_2026_05_14.md").read_text()

required_lean = [
    "structure NonPropFinalCarrierInvariant",
    "rank : ChronosCarrierData → ℕ",
    "fiberSize : ChronosCarrierData → ℕ",
    "entropyMass : ChronosCarrierData → ℚ",
    "arity : ChronosCarrierData → ℕ",
    "stratum : ChronosCarrierData → ℚ",
    "rank_positive",
    "fiber_large_from_rank",
    "entropy_mass_lower",
    "arity_agrees",
    "stratum_agrees",
    "NONPROP_INVARIANT_INTERFACE_ONLY",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "NONPROP_INVARIANT_INTERFACE_ONLY"
assert artifact["theorem_closure"] is False

for phrase in [
    "No construction of `NonPropFinalCarrierInvariant` is claimed.",
    "No `FiberLargeExists` proof is claimed.",
    "No `CountingFiberSeparation` proof is claimed.",
    "No `FiberMassBalance` proof is claimed.",
    "No `UniversalFiberEntropyGap` proof is claimed.",
    "No Chronos-RR closure is claimed.",
    "No H4.1/FGL closure is claimed.",
    "No P vs NP closure is claimed.",
    "No Clay-problem closure is claimed.",
]:
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

print("NonPropFinalCarrierInvariant interface verified.")
