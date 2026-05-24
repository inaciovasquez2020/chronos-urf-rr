from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/BlackHoleDerivedScaleValuesMap.lean"
artifact = ROOT / "artifacts/chronos/black_hole_derived_scale_values_map_2026_05_23.json"
doc = ROOT / "docs/status/BLACK_HOLE_DERIVED_SCALE_VALUES_MAP_2026_05_23.md"
runner = ROOT / "tools/run_black_hole_derived_scale_values.py"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, runner, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure BlackHoleDerivedScaleValuesMap",
    "blackHoleDerivedScaleValuesMap",
    "lightCrossingTimeFormula",
    "horizonAreaFormula",
    "surfaceGravityFormula",
    "meanDensityFormula",
    "tidalGradientFormula",
    "hawkingTemperatureFormula",
    "opticalDomainSweep",
    "black_hole_derived_scale_values_map_boundary_closed",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "DERIVED_SCALE_VALUES_ONLY_NOT_THEOREM_INPUT":
    raise SystemExit("bad status")

for token in [
    "LIGHT_CROSSING_TIME_MAP",
    "HORIZON_AREA_MAP",
    "SURFACE_GRAVITY_MAP",
    "MEAN_DENSITY_MAP",
    "TIDAL_GRADIENT_MAP",
    "HAWKING_TEMPERATURE_MAP",
    "OPTICAL_DOMAIN_SWEEP_BY_MASS_MAP",
    "light crossing time",
    "horizon area",
    "surface gravity",
    "mean density",
    "tidal gradient",
    "Hawking temperature",
    "optical domain sweep by mass",
    "not a theorem input",
    "gravity closure",
    "physical Einstein-matter flux identity",
    "restricted analytic estimate package assumptions",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    if token not in artifact.read_text():
        raise SystemExit(f"missing artifact token: {token}")
    if token not in doc.read_text():
        raise SystemExit(f"missing doc token: {token}")

if "import Chronos.Frontier.BlackHoleDerivedScaleValuesMap" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Black-hole derived scale values map verification OK.")
print("Status: DERIVED_SCALE_VALUES_ONLY_NOT_THEOREM_INPUT")
