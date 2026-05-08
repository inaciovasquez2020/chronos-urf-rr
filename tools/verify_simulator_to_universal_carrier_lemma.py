#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/CHRONOS_SIMULATOR_TO_UNIVERSAL_CARRIER_LEMMA_2026_05_08.md"
ART = ROOT / "artifacts/chronos/simulator_to_universal_carrier_lemma.json"

doc = DOC.read_text()
data = json.loads(ART.read_text())

assert data["status"] == "FRONTIER_OPEN"
assert data["theorem_closure"] is False
assert data["proves_chronos_rr_closure"] is False
assert data["lemma"] == "Simulator-to-Universal-Carrier Lemma"
assert "capacity-dominated by a registered simulator carrier" in data["statement"]

required_doc_tokens = [
    "status: FRONTIER_OPEN",
    "theorem_closure: false",
    "For every admissible carrier `C`, there exists a registered simulator carrier `r ∈ R`",
    "|T_C(b, λ)| ≤ |T_r(b, λ)|",
    "This lemma is not proved.",
    "It does not prove Uniform Carrier Subdominance.",
    "It does not prove Chronos-RR closure",
]
for token in required_doc_tokens:
    assert token in doc

print("Simulator-to-Universal-Carrier Lemma verified: FRONTIER_OPEN / STATEMENT_ONLY")
