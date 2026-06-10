#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/UniformTemporalRelaxationWaveTarget.lean"
root_import = ROOT / "lean/Chronos.lean"
doc = ROOT / "docs/status/UNIFORM_TEMPORAL_RELAXATION_WAVE_TARGET_2026_05_19.md"
artifact = ROOT / "artifacts/chronos/uniform_temporal_relaxation_wave_target_2026_05_19.json"

lean_text = lean.read_text()
root_text = root_import.read_text()
doc_text = doc.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure TemporalRelaxationWaveData",
    "structure TargetUniformTemporalRelaxationWave",
    "def UniformTemporalRelaxationWaveExistenceTarget",
    "theorem uniformTemporalRelaxationWave_from_input",
    "uniformTemporalRelaxationWave_frontier_open_marker",
    "FRONTIER_OPEN: TargetUniformTemporalRelaxationWave existence is not proved",
]

required_doc = [
    "Status: `FRONTIER_OPEN`",
    "Target isolation only.",
    "existence of TargetUniformTemporalRelaxationWave",
    "TargetUniformTemporalRelaxationWaveExistenceTarget",
    "finite-to-unrestricted relaxation lift",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for token in required_lean:
    assert token in lean_text, f"missing Lean token: {token}"

for token in required_doc:
    assert token in doc_text or token.replace("TargetUniformTemporalRelaxationWave", "UniformTemporalRelaxationWave") in doc_text, f"missing doc token: {token}"

assert "import Chronos.Frontier.UniformTemporalRelaxationWaveTarget" in root_text or "import Chronos.Frontier.TargetUniformTemporalRelaxationWaveTarget" in root_text
assert data["status"] == "FRONTIER_OPEN"
assert data["closed_object"] == "target_isolation_only"
assert data["target"] in {"TargetUniformTemporalRelaxationWaveExistenceTarget", "UniformTemporalRelaxationWaveExistenceTarget"}

for forbidden in [
    "theorem TargetUniformTemporalRelaxationWaveExistenceTarget",
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "P vs NP is proved",
    "Clay problem is solved",
    "UniversalFiberEntropyGap is proved unrestricted",
]:
    assert forbidden not in lean_text
    assert forbidden not in doc_text

for forbidden_lean in ["sorry", "admit", "axiom"]:
    assert forbidden_lean not in lean_text

print("Uniform temporal relaxation wave target verified.")
