#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/ComputableFiniteAdmissibleClass.lean"
ART = ROOT / "artifacts/chronos/computable_finite_admissible_class_2026_05_27.json"
DOC = ROOT / "docs/status/COMPUTABLE_FINITE_ADMISSIBLE_CLASS_2026_05_27.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

src = LEAN.read_text(errors="ignore")
data = json.loads(ART.read_text())
doc = DOC.read_text(errors="ignore")
root_import = ROOT_IMPORT.read_text(errors="ignore")

required_src = [
    "structure ComputableFiniteAdmissibleClass where",
    "semanticRankRate : Nat",
    "fiberEntropyGap : Nat",
    "finite_support : objectCount > 0",
    "def SemanticRankRate",
    "def FiberEntropyGap",
    "theorem semantic_rank_rate_is_computable",
    "theorem fiber_entropy_gap_is_computable",
    "theorem finite_support_positive"
]

for token in required_src:
    assert token in src, token

assert "import Chronos.Frontier.ComputableFiniteAdmissibleClass" in root_import
assert data["status"] == "COMPUTABLE_FINITE_ADMISSIBLE_CLASS_ONLY"
assert data["structural_action"] == 1
assert data["object"] == "ComputableFiniteAdmissibleClass"

for forbidden_claim in [
    "SemanticRankRate <= FiberEntropyGap",
    "finite-support bridge",
    "stability under admissible limits",
    "finite-support approximation theorem",
    "unrestricted semantic-rank-to-fiber-entropy bridge",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]:
    assert forbidden_claim in data["does_not_prove"], forbidden_claim
    assert forbidden_claim in doc, forbidden_claim

assert "COMPUTABLE_FINITE_ADMISSIBLE_CLASS_ONLY" in doc

print("COMPUTABLE_FINITE_ADMISSIBLE_CLASS_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"]
}, indent=2, sort_keys=True))
