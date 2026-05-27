import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/global_mathematical_gap_map_2026_05_27.json"
DOC = ROOT / "docs/status/GLOBAL_MATHEMATICAL_GAP_MAP_2026_05_27.md"
LEAN = ROOT / "lean/Chronos/Frontier/GlobalMathematicalGapMap.lean"


def test_gap_map_has_five_load_bearing_targets():
    data = json.loads(ART.read_text())
    assert data["status"] == "OPEN_MATHEMATICAL_GAP_MAP_ONLY"
    assert len(data["targets"]) == 5


def test_each_target_has_weakest_sufficient_object():
    data = json.loads(ART.read_text())
    for target in data["targets"]:
        assert target["weakest_sufficient_object"]
        assert "OPEN" in target["status"]


def test_no_major_claim_is_promoted():
    data = json.loads(ART.read_text())
    forbidden_promotions = {
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
    assert forbidden_promotions.issubset(set(data["does_not_prove"]))


def test_doc_and_lean_bind_same_target_names():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    lean = LEAN.read_text()
    for target in data["targets"]:
        assert target["name"] in doc
        assert target["name"] in lean
