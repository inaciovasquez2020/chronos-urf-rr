#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

doc = ROOT / "docs/status/FINITE_SINK_TO_WAVE_FRONTIER_CLUSTER_2026_05_19.md"
artifact = ROOT / "artifacts/chronos/finite_sink_to_wave_frontier_cluster_2026_05_19.json"

doc_text = doc.read_text()
artifact_text = artifact.read_text()
data = json.loads(artifact_text)

required_doc = [
    "Status: `STATUS_LOCK_ONLY`",
    "PR #411: finite sink quadratic relaxation theorem",
    "PR #412: finite rational sink quadratic relaxation theorem",
    "PR #413: finite ordered-data sink quadratic relaxation theorem",
    "PR #414: uniform temporal relaxation wave target isolated as `FRONTIER_OPEN`",
    "UniformTemporalRelaxationWaveExistenceTarget",
    "Status lock only.",
    "existence of `UniformTemporalRelaxationWave`",
    "`UniformTemporalRelaxationWaveExistenceTarget`",
    "finite-to-unrestricted relaxation lift",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for token in required_doc:
    assert token in doc_text, f"missing doc token: {token}"

assert data["status"] == "STATUS_LOCK_ONLY"
assert data["frontier_open_target"] == "UniformTemporalRelaxationWaveExistenceTarget"
assert "finite_sink_quadratic_relaxation_theorem" in data["closed_cluster"]
assert "finite_rational_sink_quadratic_relaxation_theorem" in data["closed_cluster"]
assert "finite_ordered_data_sink_quadratic_relaxation_theorem" in data["closed_cluster"]

for forbidden in [
    "UniformTemporalRelaxationWaveExistenceTarget is proved",
    "existence of UniformTemporalRelaxationWave is proved",
    "finite-to-unrestricted relaxation lift is proved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in doc_text
    assert forbidden not in artifact_text

print("Finite sink-to-wave frontier cluster verified.")
