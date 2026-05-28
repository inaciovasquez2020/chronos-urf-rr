#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/concrete_gravity_estimate_target_2026_05_28.json"
DOC = ROOT / "docs/status/CONCRETE_GRAVITY_ESTIMATE_TARGET_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteGravityEstimateTarget.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

data = json.loads(ART.read_text())

required = {
    "id": "CONCRETE_GRAVITY_ESTIMATE_TARGET_V1",
    "status": "CONCRETE_GRAVITY_ESTIMATE_TARGET_ONLY_NO_ANALYTIC_PROOF",
    "missing_analytic_lemma": "ConcreteGravityCoerciveEstimate: prove the stated curvature-energy to quasi-local-collapse coercive inequality for the selected admissible data class."
}

for key, value in required.items():
    assert data.get(key) == value, (key, data.get(key))

for key in ["estimate_statement", "assumptions", "conclusion", "boundary"]:
    assert key in data and data[key], key

boundary = set(data["boundary"])
for token in [
    "target registry only",
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
    assert token in boundary, token

doc = DOC.read_text()
for token in [
    data["status"],
    "ConcreteGravityCoerciveEstimate",
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
    "structure ConcreteGravityEstimateTarget",
    "concreteGravityEstimateTargetV1",
    "concreteGravityEstimateTargetV1_status",
    "concreteGravityEstimateTargetV1_missing_lemma",
    "concreteGravityEstimateTargetV1_boundary",
]:
    assert token in lean, token

assert "import Chronos.Frontier.ConcreteGravityEstimateTarget" in ROOT_LEAN.read_text()

print("CONCRETE_GRAVITY_ESTIMATE_TARGET_OK")
