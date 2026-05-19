from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/LyapunovDecayEnergyControl.lean"
doc = ROOT / "docs/status/LYAPUNOV_DECAY_ENERGY_CONTROL_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/lyapunov_decay_energy_control_2026_05_18.json"

for path in [lean, doc, artifact]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()

for token in [
    "def PointwiseEnergyBoundCertificate",
    "def UniformEnergyBoundCertificate",
    "def EntropyControlCertificate",
    "def UniformEntropyControlCertificate",
    "theorem energyBound_from_lyapunovDecay",
    "theorem uniformEnergyBound_from_uniformLyapunovDecay",
    "theorem entropyControl_from_lyapunovDecay_sameFunctional",
    "theorem uniformEntropyControl_from_uniformLyapunovDecay_sameFunctional",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

for token in [
    "Status: `INTERFACE_BRIDGE_ONLY`",
    "same-functional entropy-control bridge",
    "Does not prove:",
    "existence of Lyapunov decay certificates",
    "entropy production",
    "entropy monotonicity for arbitrary entropy functions",
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

print("Lyapunov decay energy-control bridge verified.")
