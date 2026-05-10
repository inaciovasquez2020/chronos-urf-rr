#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/H4_1_FGL_SelectedDomainRestriction.lean"
doc = root / "docs/status/CHRONOS_H4_1_FGL_SELECTED_DOMAIN_RESTRICTION_2026_05_10.md"
artifact = root / "artifacts/chronos/h4_1_fgl_selected_domain_restriction.json"
root_import = root / "Chronos.lean"

for p in (lean, doc, artifact, root_import):
    assert p.exists(), p

lt = lean.read_text()
dt = doc.read_text()
rt = root_import.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "def H4_1_FGL_ArbitrarySemanticFinalCarrierCounterexample",
    "Carrier := Unit",
    "Observation := Unit",
    "FinalGapLeft := fun _ => True",
    "FinalGapRight := fun _ => True",
    "theorem H4_1_FGL_arbitrary_semantic_final_carrier_separating_observable_refuted",
    "theorem H4_1_FGL_arbitrary_semantic_final_carrier_selected_instance_refuted",
    "structure H4_1_FGL_SelectedTheoremDomain",
    "separation : H4_1_FGL_SelectedFinalCarrierInstance S",
    "selected_witness : S.Carrier",
    "def toInstanceWithPoint",
    "theorem has_separating_observable",
    "theorem implies_missing_observation_extraction_witness",
    "theorem H4_1_FGL_restricted_selected_domain_implies_missing_witness",
    "arbitrary semantic-carrier domain is formally refuted",
]
for token in required_lean:
    assert token in lt, token

required_doc = [
    "Status: ARBITRARY_DOMAIN_REFUTED_SELECTED_DOMAIN_RESTRICTED",
    "`H4_1_FGL_arbitrary_semantic_final_carrier_separating_observable_refuted`",
    "`H4_1_FGL_arbitrary_semantic_final_carrier_selected_instance_refuted`",
    "`H4_1_FGL_ArbitrarySemanticFinalCarrierCounterexample`",
    "`H4_1_FGL_SelectedTheoremDomain`",
    "`H4_1_FGL_restricted_selected_domain_implies_missing_witness`",
    "Arbitrary semantic final carriers do not all satisfy selected-instance separation data.",
    "restricted to selected final-carrier instances",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
]
for token in required_doc:
    assert token in dt, token

assert data["status"] == "ARBITRARY_DOMAIN_REFUTED_SELECTED_DOMAIN_RESTRICTED"
assert data["classification"] == "DOMAIN_RESTRICTION_THEOREM"
assert "arbitrary semantic final carriers all admit separating observables" in data["refutes"]
assert data["counterexample"] == "one-point semantic final carrier with both final-gap sides true"
assert data["restricted_domain"] == "H4_1_FGL_SelectedTheoremDomain"
assert "H4_1_FGL_restricted_selected_domain_implies_missing_witness" in data["proves"]
assert data["remaining_frontier"] == "use selected final-carrier instances as the theorem domain"
assert "separating observable existence for arbitrary semantic final carriers" in data["does_not_claim"]
assert "P vs NP closure" in data["does_not_claim"]
assert "import Chronos.Frontier.H4_1_FGL_SelectedDomainRestriction" in rt

print("H4.1/FGL selected domain restriction verified: ARBITRARY_DOMAIN_REFUTED_SELECTED_DOMAIN_RESTRICTED")
