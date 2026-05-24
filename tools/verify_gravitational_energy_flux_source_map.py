#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/GravitationalEnergyFluxSourceMap.lean"
artifact = ROOT / "artifacts/chronos/gravitational_energy_flux_source_map_2026_05_23.json"
doc = ROOT / "docs/status/GRAVITATIONAL_ENERGY_FLUX_SOURCE_MAP_2026_05_23.md"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure GravitationalEnergyFluxSourceMap",
    "arxiv2605_20063_gravitationalEnergyFluxSource",
    "Teleparallel Equivalent of General Relativity",
    "Bondi-Sachs radiative space-times",
    "source_map_only_not_theorem_input",
    "gravitational_energy_flux_source_map_boundary_closed",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "SOURCE_BACKED_MAP_ONLY_NOT_THEOREM_INPUT":
    raise SystemExit("bad status")

for token in [
    "arXiv:2605.20063v1",
    "Teleparallel Equivalent of General Relativity",
    "Bondi-Sachs radiative space-times",
    "boundary surface integral",
    "physical flux-identity / flux-sign slot",
    "not a theorem input",
    "physical Einstein-matter flux identity",
    "restricted analytic estimate package assumptions",
    "unrestricted gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
    "PHYSICAL_EINSTEIN_MATTER_FLUX_IDENTITY_OR_SIGN_CERTIFICATE",
]:
    if token not in artifact.read_text():
        raise SystemExit(f"missing artifact token: {token}")
    if token not in doc.read_text():
        raise SystemExit(f"missing doc token: {token}")

if "import Chronos.Frontier.GravitationalEnergyFluxSourceMap" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Gravitational energy flux source map verification OK.")
print("Status: SOURCE_BACKED_MAP_ONLY_NOT_THEOREM_INPUT")
