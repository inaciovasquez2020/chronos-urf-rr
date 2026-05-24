#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/BlackHoleScaleNormalizationMap.lean"
artifact = ROOT / "artifacts/chronos/black_hole_scale_normalization_map_2026_05_23.json"
doc = ROOT / "docs/status/BLACK_HOLE_SCALE_NORMALIZATION_MAP_2026_05_23.md"
runner = ROOT / "tools/run_black_hole_scale_normalization.py"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, runner, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure BlackHoleScaleNormalizationMap",
    "blackHoleScaleNormalizationMap",
    "r_s = 2GM/c^2",
    "r_s ≈ 2.95325008 km per solar mass",
    "black_hole_scale_normalization_map_boundary_closed",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "SCALE_NORMALIZATION_ONLY_NOT_THEOREM_INPUT":
    raise SystemExit("bad status")

for token in [
    "2.95325008",
    "100 r_s",
    "10",
    "4.0e6",
    "6.5e9",
    "scale normalization only",
    "not a theorem input",
    "gravity closure",
    "physical Einstein-matter flux identity",
    "restricted analytic estimate package assumptions",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if token not in artifact.read_text():
        raise SystemExit(f"missing artifact token: {token}")
    if token not in doc.read_text():
        raise SystemExit(f"missing doc token: {token}")

if "import Chronos.Frontier.BlackHoleScaleNormalizationMap" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Black-hole scale normalization map verification OK.")
print("Status: SCALE_NORMALIZATION_ONLY_NOT_THEOREM_INPUT")
