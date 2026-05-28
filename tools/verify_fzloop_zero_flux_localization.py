#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/fzloop_zero_flux_localization_2026_05_28.json"
DOC = ROOT / "docs/status/FZLOOP_ZERO_FLUX_LOCALIZATION_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/FZLoopZeroFluxLocalization.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"

data = json.loads(ART.read_text())

assert data["id"] == "FZLOOP_ZERO_FLUX_LOCALIZATION_V1"
assert data["toolkit_name"] == "FZloop"
assert data["status"] == "FZLOOP_ZERO_FLUX_LOCALIZATION_PROVED_FINITE_NONNEGATIVE_MODEL_ONLY"
assert data["lean_theorem"] == "FZLoop.zero_flux_localization"

for token in [
    "finite nonnegative model only",
    "proved internal localization lemma only",
    "no Komar sign proof",
    "no Hawking mass theorem",
    "no restricted estimate proof",
    "no coercive estimate proof",
    "no analytic estimate proof",
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
    "FZloop",
    "FZLoop.zero_flux_localization",
    "finite nonnegative model lemma",
    "does not prove a Komar sign theorem",
    "Hawking mass theorem",
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
    "structure FZLoop",
    "def FZLoop.fluxSum",
    "def FZLoop.locallyZero",
    "def FZLoop.totalFlux",
    "theorem FZLoop.zero_flux_localization_list",
    "theorem FZLoop.zero_flux_localization",
    "fzLoopZeroFluxLocalizationStatus_eq",
]:
    assert token in lean, token

assert "import Chronos.Frontier.FZLoopZeroFluxLocalization" in ROOT_LEAN.read_text()

print("FZLOOP_ZERO_FLUX_LOCALIZATION_OK")
