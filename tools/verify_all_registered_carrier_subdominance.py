#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/all_registered_carrier_subdominance.json"
DOC = ROOT / "docs/status/CHRONOS_ALL_REGISTERED_CARRIER_SUBDOMINANCE_2026_05_08.md"

data = json.loads(ART.read_text())

assert data["status"] == "ALL_REGISTERED_CARRIERS_SIMULATED_ONLY"
assert data["theorem_closure"] is False
assert data["uniform_carrier_subdominance_proved"] is False
assert data["registered_admissible_carriers_all_pass"] is True
assert data["missing_theorem"] == "Simulator-to-Universal-Carrier Lemma"
assert "does not quantify over all admissible mathematical carriers" in data["boundary"]

for carrier in data["carrier_results"]:
    if carrier["admissible"]:
        assert carrier["eventual_subdominance_verified_on_range"] is True
        start = carrier["holds_from_lambda"]
        assert start is not None
        for row in carrier["rows"]:
            if row["lambda"] >= start:
                assert row["transcript_capacity"] < row["obs_dim"]
    else:
        assert carrier["eventual_subdominance_verified_on_range"] is False
        assert "obstruction-oracle" in carrier["reason_for_exclusion"]

doc = DOC.read_text()
required = [
    "ALL_REGISTERED_CARRIERS_SIMULATED_ONLY",
    "theorem_closure: false",
    "Uniform Carrier Subdominance is not proved",
    "all registered simulator carriers",
    "Simulator-to-Universal-Carrier Lemma remains missing",
]
for token in required:
    assert token in doc

print("All registered carrier subdominance verified: SIMULATED_ONLY / FRONTIER_OPEN")
