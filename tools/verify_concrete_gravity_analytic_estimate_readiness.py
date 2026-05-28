#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/concrete_gravity_analytic_estimate_readiness_2026_05_28.json"
DOC = ROOT / "docs/status/CONCRETE_GRAVITY_ANALYTIC_ESTIMATE_READINESS_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteGravityAnalyticEstimateReadiness.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

data = json.loads(ART.read_text())

assert data["id"] == "CONCRETE_GRAVITY_ANALYTIC_ESTIMATE_READINESS_V1"
assert data["status"] == "ANALYTIC_ESTIMATE_READINESS_PACKAGE_ONLY_NO_ESTIMATE_PROOF"
assert data["missing_proof"].startswith("ConcreteGravityCoerciveEstimate:")

for key in [
    "selected_data_class",
    "curvature_energy_norm",
    "quasi_local_collapse_functional",
    "boundary_flux_error",
    "readiness_items",
    "boundary",
]:
    assert data[key], key

for item in [
    "selected data class named",
    "curvature-energy norm named",
    "quasi-local collapse functional named",
    "boundary-flux error term named",
    "coercive estimate shape named",
    "missing proof isolated",
]:
    assert item in data["readiness_items"], item

for token in [
    "readiness package only",
    "no analytic estimate proof",
    "no Einstein-matter theorem",
    "no collapse theorem",
    "no Cosmic Censorship",
    "no Hoop Conjecture",
    "no quantum gravity",
    "no unrestricted Chronos-RR",
    "no unrestricted H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]:
    assert token in data["boundary"], token

doc = DOC.read_text()
for token in [
    data["status"],
    "ConcreteGravityCoerciveEstimate",
    "QL_gate(data; S) <= C * E_grav(data) + Flux_boundary(data; S)",
    "does not prove an analytic estimate",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert token in doc, token

lean = LEAN.read_text()
for token in [
    "structure ConcreteGravityAnalyticEstimateReadiness",
    "concreteGravityAnalyticEstimateReadinessV1",
    "concreteGravityAnalyticEstimateReadinessV1_status",
    "concreteGravityAnalyticEstimateReadinessV1_has_selected_data_class",
    "concreteGravityAnalyticEstimateReadinessV1_missing_proof",
    "concreteGravityAnalyticEstimateReadinessV1_boundary",
]:
    assert token in lean, token

assert "import Chronos.Frontier.ConcreteGravityAnalyticEstimateReadiness" in ROOT_LEAN.read_text()

print("CONCRETE_GRAVITY_ANALYTIC_ESTIMATE_READINESS_OK")
