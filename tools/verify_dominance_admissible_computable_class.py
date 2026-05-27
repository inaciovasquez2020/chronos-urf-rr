#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/DominanceAdmissibleComputableClass.lean"
ART = ROOT / "artifacts/chronos/dominance_admissible_computable_class_2026_05_27.json"
DOC = ROOT / "docs/status/DOMINANCE_ADMISSIBLE_COMPUTABLE_CLASS_2026_05_27.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

src = LEAN.read_text(errors="ignore")
data = json.loads(ART.read_text())
doc = DOC.read_text(errors="ignore")
root_import = ROOT_IMPORT.read_text(errors="ignore")

required_src = [
    "import Chronos.Frontier.RawAdmissibilityObstructionForComputableClass",
    "structure DominanceAdmissibleComputableClass",
    "rank_entropy_dominance",
    "def DominanceSemanticRankRate",
    "def DominanceFiberEntropyGap",
    "theorem dominance_admissible_bridge",
    "theorem dominance_admissible_finite_support",
    "theorem dominance_admissible_semantic_rank_computable",
    "theorem dominance_admissible_fiber_entropy_computable",
    "def DominanceAdmissibleToStructured",
    "theorem dominance_admissible_supplies_structured_bridge",
    "def DominanceAdmissibleReplacementLaw",
    "theorem dominance_admissible_replacement_law",
]

for token in required_src:
    assert token in src, token

assert "import Chronos.Frontier.DominanceAdmissibleComputableClass" in root_import
assert data["status"] == "DOMINANCE_ADMISSIBLE_REPLACEMENT_CLASS_CLOSED"
assert data["object"] == "DominanceAdmissibleComputableClass"

for boundary in data["does_not_prove"]:
    assert boundary in doc, boundary

print("DOMINANCE_ADMISSIBLE_COMPUTABLE_CLASS_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
