from pathlib import Path
import json

status_path = Path("docs/status/COUNTING_TO_MASS_EXACTNESS_AUDIT_2026_05_15.md")
artifact_path = Path("artifacts/chronos/counting_to_mass_exactness_audit_2026_05_15.json")

counting_path = Path("lean/Chronos/Frontier/CountingFiberSeparationFromFiberLarge.lean")
mass_path = Path("lean/Chronos/Frontier/FiberMassBalanceFromNonPropInvariant.lean")
gap_path = Path("lean/Chronos/Frontier/UniversalFiberEntropyGapFromCountingAndMass.lean")

status = status_path.read_text()
artifact_text = artifact_path.read_text()
artifact = json.loads(artifact_text)

counting = counting_path.read_text()
mass = mass_path.read_text()
gap = gap_path.read_text()

assert artifact["status"] == "EXACTNESS_GAP_ISOLATED"
assert artifact["target"] == "FiberMassBalance from CountingFiberSeparation"
assert artifact["not_currently_proved"] == "CountingFiberSeparationFromNonProp I -> FiberMassBalanceFromNonProp I"

required_status = [
    "It does not currently prove FiberMassBalanceFromNonProp from CountingFiberSeparationFromNonProp alone.",
    "CountingFiberSeparationFromNonProp I",
    "→ FiberMassBalanceFromNonProp I",
    "Strengthen CountingFiberSeparationWitness",
    "This audit does not prove:",
    "UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

required_artifact_nonclaims = {
    "CountingFiberSeparationToFiberMassBalance",
    "FiberMassBalance from counting alone",
    "UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

assert required_artifact_nonclaims.issubset(set(artifact["does_not_prove"]))

required_counting = [
    "def CountingFiberSeparationFromNonProp",
    "theorem countingFiberSeparation_from_nonprop_invariant",
]

for phrase in required_counting:
    assert phrase in counting, phrase

required_mass = [
    "def FiberMassBalanceFromNonProp",
    "theorem fiberMassBalance_from_nonprop_invariant",
    "CountingFiberSeparationFromNonProp I ∧ FiberMassBalanceFromNonProp I",
]

for phrase in required_mass:
    assert phrase in mass, phrase

required_gap = [
    "theorem universalFiberEntropyGap_from_counting_and_mass",
    "(hcount : CountingFiberSeparationFromNonProp I)",
    "(hmass : FiberMassBalanceFromNonProp I)",
]

for phrase in required_gap:
    assert phrase in gap, phrase

forbidden = [
    "CountingFiberSeparation alone proves FiberMassBalance",
    "FiberMassBalance follows from counting alone",
    "CountingFiberSeparationToFiberMassBalance is proved",
    "UniversalFiberEntropyGap is proved unconditionally",
    "Chronos-RR is proved",
    "H4.1/FGL is proved",
    "P vs NP is solved",
    "Clay problem is solved",
]

combined = status + "\n" + artifact_text

for token in forbidden:
    assert token.lower() not in combined.lower(), token

print("Counting-to-mass exactness audit verified.")
