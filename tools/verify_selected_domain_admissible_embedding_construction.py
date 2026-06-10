#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/SelectedDomainH41FGLToAdmissibleH41FGL.lean"
ARTIFACT = ROOT / "artifacts/chronos/selected_domain_admissible_embedding_construction_2026_05_18.json"
STATUS = ROOT / "docs/status/SELECTED_DOMAIN_ADMISSIBLE_EMBEDDING_CONSTRUCTION_2026_05_18.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

lean = LEAN.read_text()
artifact = json.loads(ARTIFACT.read_text())
status = STATUS.read_text()
root_imports = ROOT_IMPORT.read_text()

required_lean_tokens = [
    "def AdmissibleH41FGL (rankRate : RankRate) (fiberMass : FiberEntropyMass) : Prop :=",
    "SelectedDomainH41FGL rankRate fiberMass",
    "structure SelectedDomainAdmissibleH41FGLEmbedding",
    "def selected_domain_admissible_h41_fgl_identity_embedding",
    "theorem admissible_h41_fgl_from_selected_domain_h41_fgl_constructed",
    "theorem admissible_h41_fgl_from_restricted_h41_fgl_constructed",
    "boundary_lock := trivial",
]

for token in required_lean_tokens:
    assert token in lean, f"missing Lean token: {token}"

for forbidden in [
    "opaque AdmissibleH41FGL : Prop := False",
    "axiom selected_domain_admissible_h41_fgl_identity_embedding",
    "theorem unrestricted_h41_fgl",
    "theorem unrestricted_chronos_rr",
    "theorem p_vs_np",
    "theorem clay",
]:
    assert forbidden not in lean, f"forbidden Lean token present: {forbidden}"

assert artifact["status"] == "SELECTED_DOMAIN_ADMISSIBLE_EMBEDDING_CONSTRUCTED"

for phrase in [
    "selected-domain admissible target only",
    "restricted carrier-gap input remains explicit",
    "no unrestricted arbitrary-FiberMassData H4.1/FGL",
    "no unrestricted Chronos-RR",
    "no P vs NP",
    "no Clay closure",
]:
    assert phrase in artifact["boundary"], f"missing artifact boundary: {phrase}"

for phrase in [
    "Selected-domain admissible H4.1/FGL only.",
    "unrestricted arbitrary-`FiberMassData` H4.1/FGL",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "P vs NP",
    "any Clay problem",
]:
    assert phrase in status, f"missing status boundary: {phrase}"

assert (
    "import Chronos.Frontier.SelectedDomainH41FGLToAdmissibleH41FGL"
    in root_imports
), "root Chronos.lean does not import the module"

print("Selected-domain admissible embedding construction verified.")
