from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/CountingWitnessSupplyBridge.lean").read_text()
chronos = Path("lean/Chronos.lean").read_text()
status = Path("docs/status/COUNTING_WITNESS_SUPPLY_BRIDGE_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/counting_witness_supply_bridge_2026_05_15.json").read_text())

required_lean = [
    "CountingWitnessSupplyBridgeInput",
    "rawCountingFiberSeparationFromNonProp : Prop",
    "internal : CountingExtractionInternalStructureInput",
    "supply :",
    "SharedCountingExtractionWitnessExists internal",
    "RawCountingSeparationSuppliesSharedWitness",
    "raw_counting_separation_supplies_shared_witness",
    "RawCountingSeparationSuppliesStructuredNonPropInvariant",
    "raw_counting_separation_supplies_structured_nonprop_invariant",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.CountingWitnessSupplyBridge" in chronos

assert artifact["status"] == "CONDITIONAL_WITNESS_SUPPLY_BRIDGE_CLOSED"
assert artifact["minimal_missing_lemma"] == (
    "rawCountingFiberSeparationFromNonProp -> "
    "SharedCountingExtractionWitnessExists internal"
)

required_status = [
    "Status: CONDITIONAL_WITNESS_SUPPLY_BRIDGE_CLOSED",
    "Minimal Missing Lemma",
    "rawCountingFiberSeparationFromNonProp →",
    "SharedCountingExtractionWitnessExists internal",
    "Conditional: this requires a supply map from raw counting separation to the shared witness.",
]

for phrase in required_status:
    assert phrase in status, phrase

forbidden = [
    "proves the supply map exists",
    "proves raw Prop-only extraction",
    "proves ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp",
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

print("Counting witness supply bridge verified.")
