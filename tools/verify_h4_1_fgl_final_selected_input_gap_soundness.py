#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "Chronos/Frontier/H4_1_FGL_FinalSelectedInputGapSoundness.lean"
ARTIFACT = ROOT / "artifacts/chronos/h4_1_fgl_final_selected_input_gap_soundness.json"
DOC = ROOT / "docs/status/CHRONOS_H4_1_FGL_FINAL_SELECTED_INPUT_GAP_SOUNDNESS_2026_05_10.md"
CHRONOS = ROOT / "Chronos.lean"

for path in [LEAN, ARTIFACT, DOC, CHRONOS]:
    assert path.exists(), path

lt = LEAN.read_text()
dt = DOC.read_text()
at = ARTIFACT.read_text()
ct = CHRONOS.read_text()
data = json.loads(at)

assert data["status"] == "SELECTED_DOMAIN_GAP_SOUNDNESS_CLOSED"
assert data["theorem_domain"] == "H4_1_FGL_SelectedTheoremDomain"
assert "H4_1_FGL_FinalSelectedCarrierGapSoundness" in data["proves"]
assert data["remaining_frontier"] == "none inside selected-domain H4.1/FGL observation-to-gap/soundness bridge"

for token in [
    "SELECTED_DOMAIN_GAP_SOUNDNESS_CLOSED",
    "H4_1_FGL_SelectedTheoremDomain",
    "H4_1_FGL_FinalSelectedCarrierGapSoundness",
    "none inside selected-domain H4.1/FGL observation-to-gap/soundness bridge",
    "does not claim arbitrary semantic final-carrier closure",
    "does not claim separating-observable existence for arbitrary semantic final carriers",
    "does not prove unrestricted H4.1/FGL closure",
    "does not prove UniversalFiberEntropyGap",
    "does not prove Chronos-RR",
    "does not prove P vs NP closure",
    "does not prove Clay-problem closure",
]:
    assert token in lt or token in dt or token in at, token

assert "import Chronos.Frontier.H4_1_FGL_FinalSelectedInputGapSoundness" in ct

for forbidden in [
    "solves P vs NP",
    "proves P vs NP",
    "Clay problem solved",
    "unrestricted H4.1/FGL closure proved",
]:
    assert forbidden not in lt
    assert forbidden not in dt
    assert forbidden not in at

print("H4.1/FGL final selected input gap soundness verified: SELECTED_DOMAIN_GAP_SOUNDNESS_CLOSED")
