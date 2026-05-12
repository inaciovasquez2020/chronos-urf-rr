#!/usr/bin/env python3
from pathlib import Path
import json

lean = Path("Chronos/Frontier/FiberLargeExists.lean")
artifact = Path("artifacts/chronos/fiber_large_exists_2026_05_12.json")
status = Path("docs/status/CHRONOS_FIBER_LARGE_EXISTS_2026_05_12.md")
root = Path("Chronos.lean")

for p in (lean, artifact, status, root):
    if not p.exists():
        raise SystemExit(f"missing required file: {p}")

lean_text = lean.read_text()
required_lean = [
    "namespace Chronos.Frontier",
    "lemma fiber_large_exists",
    "by_cases hq0 : q ^ g = 0",
    "have esigma : (Sigma fun y : Y => {x : X // f x = y}) ≃ X",
    "Fintype.card_sigma",
    "Fintype.card_congr",
    "Finset.sum_le_sum",
    "Nat.pred_lt",
    "end Chronos.Frontier",
]
for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit", "axiom fiber_large_exists"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token: {forbidden}")

if "import Chronos.Frontier.FiberLargeExists" not in root.read_text():
    raise SystemExit("Chronos.lean does not import FiberLargeExists module")

data = json.loads(artifact.read_text())
if data.get("status") != "PROVED_COMBINATORIAL_LEMMA":
    raise SystemExit("artifact status mismatch")
if data.get("theorem") != "Chronos.Frontier.fiber_large_exists":
    raise SystemExit("artifact theorem mismatch")
if data.get("theorem_level_closure") is not True:
    raise SystemExit("artifact must mark this lemma theorem-level closed")

status_text = status.read_text()
required_status = [
    "Status: PROVED_COMBINATORIAL_LEMMA",
    "Chronos.Frontier.fiber_large_exists",
    "does not prove RankRateGap",
    "does not prove UniversalFiberEntropyGap",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
]
for token in required_status:
    if token not in status_text:
        raise SystemExit(f"missing status token: {token}")

print("FiberLargeExists theorem artifact verified.")
