from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/RestrictedRateThickToRecoveryRouteSurfaces.lean"
doc = ROOT / "docs/status/RESTRICTED_RATE_THICK_TO_RECOVERY_ROUTE_SURFACES_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/restricted_rate_thick_to_recovery_route_surfaces_2026_05_18.json"

for path in [lean, doc, artifact]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_text = artifact.read_text()

for token in [
    "def RestrictedUniversalFiberEntropyGapRoute",
    "def RestrictedChronosRRRecoveryBridge",
    "def RestrictedH41FGLRecoveryBridge",
    "theorem restrictedUniversalFiberEntropyGapRoute_from_restrictedRateThickCoercivity",
    "theorem restrictedChronosRRRecoveryBridge_from_restrictedUniversalFiberEntropyGapRoute",
    "theorem restrictedH41FGLRecoveryBridge_from_restrictedChronosRRRecoveryBridge",
    "theorem restrictedChronosRRRecoveryBridge_from_restrictedRateThickCoercivity",
    "theorem restrictedH41FGLRecoveryBridge_from_restrictedRateThickCoercivity",
    "theorem restrictedRecoveryRoute_from_uniformEntropyControl",
    "theorem restrictedRecoveryRoute_from_uniformLyapunovDecay_sameFunctional",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

for forbidden in ["sorry", "admit"]:
    if forbidden in lean_text:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")

for token in [
    "Status: `INTERFACE_BRIDGE_ONLY`",
    "restricted rate-thick coercivity",
    "restricted UniversalFiberEntropyGap route",
    "restricted Chronos-RR recovery bridge",
    "restricted H4.1/FGL recovery bridge",
    "Does not prove:",
    "existence of admissible dissipation certificates",
    "construction of an admissible domain",
    "entropy production",
    "entropy monotonicity for arbitrary entropy functions",
    "unrestricted rate-thick coercivity",
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

print("Restricted rate-thick to recovery route surfaces verified.")
