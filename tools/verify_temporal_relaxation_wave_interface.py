from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/TemporalRelaxationWaveInterface.lean"
doc = ROOT / "docs/status/TEMPORAL_RELAXATION_WAVE_INTERFACE_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/temporal_relaxation_wave_interface_2026_05_18.json"

for path in [lean, doc, artifact]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()

required_lean = [
    "def TemporalRelaxationWave",
    "def UniformTemporalRelaxationWave",
    "theorem temporalRelaxationWave_from_uniformDecay",
    "theorem unit_uniformTemporalRelaxationWave",
]

for token in required_lean:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

required_boundary = [
    "Status: `INTERFACE_ONLY`",
    "Does not prove:",
    "physical time travel",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for token in required_boundary:
    if token not in doc_text:
        raise SystemExit(f"missing boundary token: {token}")

if '"status": "INTERFACE_ONLY"' not in artifact_text:
    raise SystemExit("artifact status is not INTERFACE_ONLY")

print("Temporal relaxation wave interface verified.")
