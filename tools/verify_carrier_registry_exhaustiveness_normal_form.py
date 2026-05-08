#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/CHRONOS_CARRIER_REGISTRY_EXHAUSTIVENESS_NORMAL_FORM_2026_05_08.md"
ART = ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_normal_form.json"
SIM = ROOT / "artifacts/chronos/all_registered_carrier_subdominance.json"
doc = DOC.read_text()
data = json.loads(ART.read_text())
sim = json.loads(SIM.read_text())
assert data["status"] == "FRONTIER_OPEN"
assert data["theorem_closure"] is False
assert data["uniform_carrier_subdominance_proved"] is False
assert data["proves_chronos_rr_closure"] is False
assert data["missing_theorem"] == "Carrier Registry Exhaustiveness Theorem"
registered = set(data["registered_subdominant_classes"])
forbidden = set(data["forbidden_boundary_classes"])
sim_admissible = {c["name"] for c in sim["carrier_results"] if c["admissible"]}
sim_forbidden = {c["name"] for c in sim["carrier_results"] if not c["admissible"]}
assert sim_admissible == registered
assert forbidden <= sim_forbidden
required_doc_tokens = [
"status: FRONTIER_OPEN",
"theorem_closure: false",
"Every admissible carrier has a transcript normal form dominated by one of the registered subdominant classes.",
"It does not prove registry exhaustiveness.",
"It does not prove Uniform Carrier Subdominance.",
"It does not prove Chronos-RR closure",
]
for token in required_doc_tokens:
    assert token in doc
print("Carrier registry exhaustiveness normal form verified: FRONTIER_OPEN / NORMAL_FORM_TARGET_ONLY")
