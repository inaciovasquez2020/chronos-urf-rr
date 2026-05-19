from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/TemporalRelaxationWaveLyapunovBridge.lean"
doc = ROOT / "docs/status/TEMPORAL_RELAXATION_WAVE_LYAPUNOV_BRIDGE_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/temporal_relaxation_wave_lyapunov_bridge_2026_05_18.json"

for path in [lean, doc, artifact]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()

for token in [
    "def LyapunovDecayCertificate",
    "def UniformLyapunovDecayCertificate",
    "theorem lyapunovDecay_from_temporalRelaxationWave",
    "theorem uniformLyapunovDecay_from_uniformTemporalRelaxationWave",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

for token in [
    "Status: `INTERFACE_BRIDGE_ONLY`",
    "Does not prove:",
    "existence of temporal relaxation waves",
    "physical time travel",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if token not in doc_text:
        raise SystemExit(f"missing boundary token: {token}")

if '"status": "INTERFACE_BRIDGE_ONLY"' not in artifact_text:
    raise SystemExit("artifact status is not INTERFACE_BRIDGE_ONLY")

print("Temporal relaxation wave Lyapunov bridge verified.")
