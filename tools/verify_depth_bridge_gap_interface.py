#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/depth_bridge_gap_interface.json"
DOC = ROOT / "docs/status/CHRONOS_DEPTH_BRIDGE_GAP_INTERFACE_2026_05_08.md"
LEAN = ROOT / "Chronos/Frontier/DepthBridgeFiberGap.lean"

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["status"] == "CONDITIONAL_INTERFACE_ONLY"
assert data["theorem_closure"] is False
assert data["chronos_rr_closure"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False
assert data["missing_object"] == "FiberEntropyGap"

for token in [
    "structure DepthBridgeInstance",
    "structure FiberEntropyGap",
    "structure RankImageBound",
    "def depthBridgeFiberGap_to_rankImageBound",
    "eventually_rank_bound := G.eventually_gap",
]:
    assert token in lean

for token in [
    "status: CONDITIONAL_INTERFACE_ONLY",
    "FiberEntropyGap -> RankImageBound",
    "does not prove FiberEntropyGap",
    "does not prove the Depth Bridge",
    "does not prove Chronos-RR closure",
    "does not prove H4.1/FGL closure",
    "does not prove P vs NP",
]:
    assert token in doc

for forbidden in [
    "theorem_closure: true",
    "Chronos-RR closure is proved",
    "H4.1/FGL closure is proved",
    "P vs NP is proved",
]:
    assert forbidden not in doc
    assert forbidden not in json.dumps(data)

subprocess.run(
    ["lake", "env", "lean", "Chronos/Frontier/DepthBridgeFiberGap.lean"],
    cwd=ROOT,
    check=True,
)

print("Depth Bridge gap interface verified: CONDITIONAL_INTERFACE_ONLY")
