from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/CountingExtractionPropOnlyObstruction.lean").read_text()
chronos = Path("lean/Chronos.lean").read_text()
status = Path("docs/status/COUNTING_EXTRACTION_PROP_ONLY_OBSTRUCTION_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/counting_extraction_prop_only_obstruction_2026_05_15.json").read_text())

required_lean = [
    "PropOnlyCountingSeparationExtractionClaim",
    "prop_only_counting_separation_extraction_obstructed",
    "exact h True False True",
    "CountingSeparationExtractionWitnessInput",
    "CountingSeparationExtractionWitnessSufficient",
    "counting_separation_extraction_witness_sufficient",
    "witness : countingFiberSeparationFromNonProp → nonPropInvariant",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.CountingExtractionPropOnlyObstruction" in chronos

assert artifact["status"] == "PROP_ONLY_EXTRACTION_OBSTRUCTED"
assert artifact["closed_result"] == "PropOnlyCountingSeparationExtractionClaim is false."
assert artifact["counterexample"]["countingFiberSeparationFromNonProp"] == "True"
assert artifact["counterexample"]["nonPropInvariant"] == "False"

required_status = [
    "Status: PROP_ONLY_EXTRACTION_OBSTRUCTED",
    "The Prop-only extraction claim is false",
    "countingFiberSeparationFromNonProp := True",
    "nonPropInvariant := False",
    "A genuine extraction witness",
    "This does not prove ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp.",
]

for phrase in required_status:
    assert phrase in status, phrase

forbidden = [
    "proves ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp",
    "proves the extraction witness exists",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves unrestricted Chronos-RR",
    "proves unrestricted H4.1/FGL",
    "proves P vs NP",
    "solves P vs NP",
    "solves any Clay problem",
]

combined = (lean + "\n" + status + "\n" + json.dumps(artifact)).lower()

for token in forbidden:
    assert token.lower() not in combined, token

print("Counting extraction Prop-only obstruction verified.")
