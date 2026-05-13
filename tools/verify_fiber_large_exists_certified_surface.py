#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean = (ROOT / "Chronos/Frontier/FiberLargeExistsCertifiedSurface.lean").read_text()
root = (ROOT / "Chronos.lean").read_text()
doc = (ROOT / "docs/status/CHRONOS_FIBER_LARGE_EXISTS_CERTIFIED_SURFACE_2026_05_13.md").read_text()
artifact = json.loads(
    (ROOT / "artifacts/chronos/fiber_large_exists_certified_surface_2026_05_13.json").read_text()
)

required = [
    "import Chronos.Frontier.FiberLargeExists",
    "FiberLargeExistsCertifiedSurfaceStatus",
    "frontier_open_preserved",
    "SemanticRankRateToFiberEntropySoundnessConditionalOnly",
    "semanticRankRateToFiberEntropySoundness_conditional_only",
    "NonPropRankEntropyWitness",
]

for token in required:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit", "axiom"]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

if "import Chronos.Frontier.FiberLargeExistsCertifiedSurface" not in root:
    raise SystemExit("missing root import")

if artifact["status"] != "CERTIFIED_SURFACE_ONLY":
    raise SystemExit("bad status")

if artifact["frontier_open_preserved"] is not True:
    raise SystemExit("FRONTIER_OPEN not preserved")

if artifact["theorem_level_closure"] is not False:
    raise SystemExit("theorem closure must remain false")

for token in [
    "FRONTIER_OPEN is preserved.",
    "No unrestricted UniversalFiberEntropyGap theorem is claimed.",
    "No Chronos-RR theorem closure is claimed.",
    "No H4.1/FGL closure is claimed.",
    "No P vs NP closure is claimed.",
    "No Clay-problem closure is claimed.",
]:
    if token not in doc:
        raise SystemExit(f"missing boundary token: {token}")

print("FiberLargeExists certified surface status verified.")
