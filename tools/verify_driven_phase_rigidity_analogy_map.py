#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/DrivenPhaseRigidityAnalogyMap.lean"
artifact = ROOT / "artifacts/chronos/driven_phase_rigidity_analogy_map_2026_05_23.json"
doc = ROOT / "docs/status/DRIVEN_PHASE_RIGIDITY_ANALOGY_MAP_2026_05_23.md"
root_import = ROOT / "lean/Chronos.lean"

for path in [lean, artifact, doc, root_import]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

lean_text = lean.read_text()
for token in [
    "structure DrivenPhaseRigidityAnalogyMap",
    "DrivenPhaseRigidityExternalSourceRecord",
    "scienceDailyFluxSwitchingFloquetRecord",
    "drivenPhaseRigidityAnalogyWitness",
    "analogy_only_not_theorem_input",
    "driven_phase_rigidity_analogy_map_boundary_closed",
]:
    if token not in lean_text:
        raise SystemExit(f"missing Lean token: {token}")

data = json.loads(artifact.read_text())
if data["status"] != "SOURCE_BACKED_ANALOGY_ONLY_NOT_THEOREM_INPUT":
    raise SystemExit("bad status")

for token in [
    "ScienceDaily",
    "Flux-switching Floquet engineering",
    "time-dependent driving",
    "topological phase diagrams",
    "not theorem input",
    "not empirical validation of URF",
    "not empirical validation of Chronos",
    "Chronos-RR",
    "H4.1/FGL",
    "gravity closure",
    "physical Einstein-matter flux identity",
    "P vs NP",
    "any Clay problem",
]:
    if token not in artifact.read_text():
        raise SystemExit(f"missing artifact token: {token}")
    if token not in doc.read_text():
        raise SystemExit(f"missing doc token: {token}")

if "import Chronos.Frontier.DrivenPhaseRigidityAnalogyMap" not in root_import.read_text():
    raise SystemExit("missing Chronos root import")

print("Driven phase rigidity analogy map verification OK.")
print("Status: SOURCE_BACKED_ANALOGY_ONLY_NOT_THEOREM_INPUT")
