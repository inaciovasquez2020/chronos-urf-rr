from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/CountingExtractionInternalStructure.lean").read_text()
chronos = Path("lean/Chronos.lean").read_text()
status = Path("docs/status/COUNTING_EXTRACTION_INTERNAL_STRUCTURE_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/counting_extraction_internal_structure_2026_05_15.json").read_text())

required_lean = [
    "CountingExtractionInternalStructureInput",
    "Witness : Type",
    "ValidExtractionWitness : Witness → Prop",
    "StructuredCountingFiberSeparationFromNonProp",
    "StructuredNonPropInvariant",
    "SharedCountingExtractionWitnessExists",
    "structured_counting_separation_to_shared_witness",
    "shared_witness_to_structured_nonprop_invariant",
    "structured_counting_extraction_to_nonprop_invariant",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.CountingExtractionInternalStructure" in chronos

assert artifact["status"] == "STRUCTURED_EXTRACTION_SURFACE_CLOSED"
assert artifact["internal_structures"]["shared_witness"] == "W : Witness"

required_status = [
    "Status: STRUCTURED_EXTRACTION_SURFACE_CLOSED",
    "Witness : Type",
    "ValidExtractionWitness : Witness → Prop",
    "StructuredCountingFiberSeparationFromNonProp I :=",
    "StructuredNonPropInvariant I :=",
    "SharedCountingExtractionWitnessExists I :=",
    "This does not prove raw Prop-only extraction.",
]

for phrase in required_status:
    assert phrase in status, phrase

forbidden = [
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

print("Counting extraction internal structure verified.")
