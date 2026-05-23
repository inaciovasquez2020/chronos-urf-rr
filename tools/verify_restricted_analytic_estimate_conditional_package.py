#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/RestrictedAnalyticEstimateConditionalPackage.lean"
artifact = ROOT / "artifacts/chronos/restricted_analytic_estimate_conditional_package_2026_05_23.json"
doc = ROOT / "docs/status/RESTRICTED_ANALYTIC_ESTIMATE_CONDITIONAL_PACKAGE_2026_05_23.md"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure RestrictedAnalyticEstimateData",
    "theorem restricted_concentration_monotonicity",
    "theorem restricted_continuation_norm_control",
    "ConcreteAnalyticEinsteinMatterEstimatePackage",
    "numericalRestrictedAnalyticEstimateData",
    "N := fun _ => (5 : ℝ≥0∞)",
    "Qstar := 1",
    "C := (10 : ℝ≥0∞)",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "CONDITIONAL_PACKAGE_WITH_NUMERICAL_SANITY_WITNESS":
    raise SystemExit("bad status")

for token in [
    "physical Einstein-matter flux identity",
    "unrestricted gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if token not in artifact.read_text():
        raise SystemExit(f"missing artifact boundary: {token}")
    if token not in doc.read_text():
        raise SystemExit(f"missing doc boundary: {token}")

if "import Chronos.Frontier.RestrictedAnalyticEstimateConditionalPackage" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Restricted analytic estimate conditional package verification OK.")
print("Status: CONDITIONAL_PACKAGE_WITH_NUMERICAL_SANITY_WITNESS")
