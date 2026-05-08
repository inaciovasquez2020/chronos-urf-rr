#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/depth_bridge_fiber_gap_frontier.json"
DOC = ROOT / "docs/status/CHRONOS_DEPTH_BRIDGE_FIBER_GAP_FRONTIER_2026_05_08.md"
data = json.loads(ART.read_text())
doc = DOC.read_text()
assert data["status"] == "FRONTIER_OPEN"
assert data["theorem_closure"] is False
assert data["chronos_rr_closure"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False
assert data["proved_here"] is False
assert data["weakest_missing_lemma"] == "Depth Bridge Fiber Entropy Gap"
required_constraints = [
"uniform_positive_conditional_entropy_gap",
"subexponential_fiber_multiplicity_distortion",
"registry_uniform_obstruction_gap",
"rank_image_defect_survives_scaling",
"no_factorization_through_vanishing_fibers",
]
assert data["fiber_constraints"] == required_constraints
required_doc_tokens = [
"status: FRONTIER_OPEN",
"theorem_closure: false",
"Depth Bridge Fiber Entropy Gap",
"H(O_lambda | T_C(lambda)) >= alpha * dim(O_lambda)",
"liminf_{lambda -> infinity}",
"does not prove the Depth Bridge",
"does not prove Chronos-RR closure",
"does not prove H4.1/FGL closure",
"does not prove P vs NP",
]
for token in required_doc_tokens:
    assert token in doc
for forbidden in [
"Chronos-RR closure is proved",
"H4.1/FGL closure is proved",
"P vs NP is proved",
"theorem_closure: true",
]:
    assert forbidden not in doc
    assert forbidden not in json.dumps(data)
print("Depth Bridge fiber gap frontier verified: FRONTIER_OPEN / STATEMENT_ONLY")
