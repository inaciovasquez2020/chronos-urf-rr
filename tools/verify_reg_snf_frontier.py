#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/CHRONOS_REG_SNF_FRONTIER_2026_05_08.md"
ART = ROOT / "artifacts/chronos/reg_snf_frontier.json"

doc = DOC.read_text()
data = json.loads(ART.read_text())

assert data["status"] == "FRONTIER_OPEN"
assert data["theorem_closure"] is False
assert data["lemma"] == "Reg-SNF"
assert data["weakest_missing_lemma"] is True
assert data["proves_registry_exhaustiveness"] is False
assert data["proves_uniform_carrier_subdominance"] is False
assert data["proves_non_factorization"] is False
assert data["proves_chronos_rr_closure"] is False

required = [
    "status: FRONTIER_OPEN",
    "theorem_closure: false",
    "Carrier Admissibility implies Registered Subdominant Normal Form.",
    "∀ admissible C, ∃ r ∈ R, ∀ b,λ:",
    "It does not prove Reg-SNF.",
    "It does not prove Chronos-RR closure",
]

for token in required:
    assert token in doc

print("Reg-SNF frontier verified: FRONTIER_OPEN / WEAKEST_MISSING_LEMMA_ONLY")
