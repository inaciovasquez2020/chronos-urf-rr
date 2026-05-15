from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/CountingSeparationNonPropInvariantExtraction.lean").read_text()
chronos = Path("lean/Chronos.lean").read_text()
status = Path("docs/status/COUNTING_SEPARATION_NONPROP_INVARIANT_EXTRACTION_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/counting_separation_nonprop_invariant_extraction_2026_05_15.json").read_text())

required_lean = [
    "CountingSeparationNonPropInvariantInput",
    "CountingSeparationSuppliesNonPropInvariant",
    "counting_separation_supplies_nonprop_invariant",
    "CountingSeparationToMassViaNonPropInvariantInput",
    "CountingSeparationToMassViaNonPropInvariant",
    "counting_separation_to_mass_via_nonprop_invariant",
    "extraction : countingFiberSeparationFromNonProp → nonPropInvariant",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.CountingSeparationNonPropInvariantExtraction" in chronos

assert artifact["status"] == "THEOREM_TARGET_ISOLATED"
assert "supplies the NonProp invariant" in artifact["minimal_missing_lemma"]

required_status = [
    "Status: THEOREM_TARGET_ISOLATED",
    "Minimal Missing Lemma",
    "countingFiberSeparationFromNonProp → nonPropInvariant",
    "This does not prove ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp unless the extraction hypothesis is supplied.",
]

for phrase in required_status:
    assert phrase in status, phrase

forbidden = [
    "proves unrestricted UniversalFiberEntropyGap",
    "proves unrestricted Chronos-RR",
    "proves unrestricted H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves a Clay problem",
]

combined = (lean + "\n" + status + "\n" + json.dumps(artifact)).lower()

for token in forbidden:
    assert token.lower() not in combined, token

assert (
    "does not prove ordinary countingfiberseparationfromnonprop alone implies "
    "fibermassbalancefromnonprop unless the extraction hypothesis is supplied"
) in combined

print("Counting separation NonProp invariant extraction target verified.")
