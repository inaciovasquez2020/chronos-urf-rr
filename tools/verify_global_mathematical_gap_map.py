#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/global_mathematical_gap_map_2026_05_27.json"
DOC = ROOT / "docs/status/GLOBAL_MATHEMATICAL_GAP_MAP_2026_05_27.md"
LEAN = ROOT / "lean/Chronos/Frontier/GlobalMathematicalGapMap.lean"

data = json.loads(ART.read_text())

assert data["id"] == "GLOBAL_MATHEMATICAL_GAP_MAP_2026_05_27"
assert data["status"] == "OPEN_MATHEMATICAL_GAP_MAP_ONLY"
assert data["claim_type"] == "mathematical_missing_object_registry"

targets = data["targets"]
assert len(targets) == 5

required_targets = {
    "RankEntropyGapLemma",
    "FiniteToUniformUpgradeLemma",
    "LocalToGlobalRigidityTransferLemma",
    "BoundaryCompactnessCollapseControlLemma",
    "DfmMkcExecutablePredictionBinding",
}

assert {target["name"] for target in targets} == required_targets

for target in targets:
    assert target["weakest_sufficient_object"]
    assert target["status"] in {
        "OPEN_MATHEMATICAL_GAP",
        "OPEN_MATHEMATICAL_COMPUTATION_GAP",
    }

required_boundaries = {
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted gravity closure",
}

assert required_boundaries.issubset(set(data["does_not_prove"]))

doc = DOC.read_text()
lean = LEAN.read_text()

for token in required_targets:
    assert token in doc
    assert token in lean

for token in required_boundaries:
    assert token in doc

assert "globalMathematicalGapTargets_length" in lean
assert "globalBoundaryTokens_length" in lean

print("GLOBAL_MATHEMATICAL_GAP_MAP_OK")
