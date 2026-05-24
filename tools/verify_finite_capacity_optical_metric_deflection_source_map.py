#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteCapacityOpticalMetricDeflectionSourceMap.lean"
artifact = ROOT / "artifacts/chronos/finite_capacity_optical_metric_deflection_source_map_2026_05_23.json"
doc = ROOT / "docs/status/FINITE_CAPACITY_OPTICAL_METRIC_DEFLECTION_SOURCE_MAP_2026_05_23.md"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure FiniteCapacityOpticalMetricDeflectionSourceMap",
    "vasquezFiniteCapacityOpticalMetricDeflectionSource",
    "n(r) = alpha(r)^(-1/2)",
    "d_r n(r) > 0",
    "d_r alpha(r) < 0",
    "n(r) = 1 - epsilon * exp(-r/R)",
    "source_map_only_not_theorem_input",
    "finite_capacity_optical_metric_deflection_source_map_boundary_closed",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "SOURCE_BACKED_MAP_ONLY_NOT_THEOREM_INPUT":
    raise SystemExit("bad status")

for token in [
    "finite capacity",
    "bounded information transport",
    "bounded amplification of gradients",
    "finite operational resolution",
    "optical metrics",
    "outward deflection",
    "without exotic matter",
    "n(r) = alpha(r)^(-1/2)",
    "d_r n(r) > 0",
    "d_r alpha(r) < 0",
    "n(r) = 1 - epsilon * exp(-r/R)",
    "not a theorem input",
    "gravity closure",
    "physical Einstein-matter flux identity",
    "restricted analytic estimate package assumptions",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
    "FINITE_CAPACITY_OPTICAL_METRIC_DEFLECTION_FORMAL_THEOREM_OR_EXTERNAL_CITATION",
]:
    if token not in artifact.read_text():
        raise SystemExit(f"missing artifact token: {token}")
    if token not in doc.read_text():
        raise SystemExit(f"missing doc token: {token}")

if "import Chronos.Frontier.FiniteCapacityOpticalMetricDeflectionSourceMap" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Finite capacity optical metric deflection source map verification OK.")
print("Status: SOURCE_BACKED_MAP_ONLY_NOT_THEOREM_INPUT")
