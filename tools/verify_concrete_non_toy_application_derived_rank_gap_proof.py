import json
from pathlib import Path

ART = Path("artifacts/chronos/concrete_non_toy_application_derived_rank_gap_proof_2026_05_28.json")
DOC = Path("docs/status/CONCRETE_NON_TOY_APPLICATION_DERIVED_RANK_GAP_PROOF_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/ConcreteNonToyApplicationDerivedRankGapProof.lean")

required = [
    "unrestricted rank entropy gap",
    "finite-to-uniform upgrade",
    "UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["status"] == "CONCRETE_PROOF_OBJECT_INTERFACE_ONLY"
for token in required:
    assert token in doc
    assert token in data["does_not_prove"]
for token in [
    "concrete_non_toy_application_exports_rank_gap",
    "concrete_non_toy_application_exports_non_toy",
]:
    assert token in lean

print("CONCRETE_NON_TOY_APPLICATION_DERIVED_RANK_GAP_PROOF_OK")
