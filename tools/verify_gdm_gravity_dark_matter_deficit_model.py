#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/gdm_gravity_dark_matter_deficit_model_2026_05_28.json"
DOC = ROOT / "docs/status/GDM_GRAVITY_DARK_MATTER_DEFICIT_MODEL_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/GDMGravityDarkMatterDeficitModel.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

data = json.loads(ART.read_text())

assert data["id"] == "GDM_GRAVITY_DARK_MATTER_DEFICIT_MODEL_V1"
assert data["toolkit_name"] == "GDM"
assert data["status"] == "GDM_DEFICIT_ACCOUNTING_MODEL_PROVED_FINITE_NONNEGATIVE_ONLY"
assert data["core_identity"] == "effectiveMass = baryonicMass + geometricDeficitMass"

for theorem in [
    "GDM.baryonic_le_effective",
    "GDM.zero_deficit_effective_eq_baryonic",
    "GDM.positive_deficit_effective_gt_baryonic",
    "GDM.effective_eq_baryonic_implies_zero_deficit",
]:
    assert theorem in data["proved_theorems"], theorem

for token in [
    "finite nonnegative accounting model only",
    "internal theorem only",
    "no observational evidence",
    "no galaxy rotation curve fit",
    "no lensing fit",
    "no dark matter replacement",
    "no Lambda-CDM refutation",
    "no modified gravity theorem",
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
    assert token in data["boundary"], token

doc = DOC.read_text()
for token in [
    data["status"],
    "GDM",
    "Gravity Dark Matter",
    "Geometric Deficit Mass",
    "effectiveMass = baryonicMass + geometricDeficitMass",
    "GDM.positive_deficit_effective_gt_baryonic",
    "does not provide observational evidence",
    "dark matter replacement",
    "Lambda-CDM refutation",
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
    "structure GDMData",
    "def effectiveMass",
    "def residualMass",
    "theorem baryonic_le_effective",
    "theorem zero_deficit_effective_eq_baryonic",
    "theorem positive_deficit_effective_gt_baryonic",
    "theorem effective_eq_baryonic_implies_zero_deficit",
    "theorem status_eq",
]:
    assert token in lean, token

assert "import Chronos.Frontier.GDMGravityDarkMatterDeficitModel" in ROOT_LEAN.read_text()

print("GDM_GRAVITY_DARK_MATTER_DEFICIT_MODEL_OK")
