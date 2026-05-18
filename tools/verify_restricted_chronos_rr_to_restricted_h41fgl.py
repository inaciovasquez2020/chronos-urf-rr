#!/usr/bin/env python3
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/RestrictedChronosRRToRestrictedH41FGL.lean"
DOC = ROOT / "docs/status/RESTRICTED_CHRONOS_RR_TO_RESTRICTED_H41FGL_2026_05_18.md"
ART = ROOT / "artifacts/chronos/restricted_chronos_rr_to_restricted_h41fgl_2026_05_18.json"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
for path in [LEAN, DOC, ART, ROOT_IMPORT]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
lean = LEAN.read_text(); doc = DOC.read_text(); artifact_text = ART.read_text(); artifact = json.loads(artifact_text); root_import = ROOT_IMPORT.read_text()
for token in ["abbrev RestrictedChronosRR", "structure RestrictedH41FGLWitness", "rr_certificate : RestrictedChronosRR D", "boundary_lock : UnrestrictedChronosRRFrontierOpen", "def RestrictedH41FGL", "theorem restricted_chronos_rr_to_restricted_h41_fgl", "RestrictedChronosRR D", "RestrictedH41FGL D", "unrestricted_chronos_rr_frontier_open"]:
    if token not in lean:
        raise SystemExit(f"missing Lean token: {token}")
for forbidden in ["admit", "sorry", "axiom", "def H41FGL", "structure H41FGL", "theorem unrestricted_chronos_rr ", "theorem unrestricted_h41_fgl"]:
    if forbidden in lean:
        raise SystemExit(f"forbidden Lean token present: {forbidden}")
if "import Chronos.Frontier.RestrictedChronosRRToRestrictedH41FGL" not in root_import:
    raise SystemExit("missing Chronos.lean import")
if artifact.get("status") != "RESTRICTED_CHRONOS_RR_TO_RESTRICTED_H41FGL_CLOSED":
    raise SystemExit("incorrect artifact status")
if artifact.get("closed_theorem") != "restricted_chronos_rr_to_restricted_h41_fgl":
    raise SystemExit("incorrect closed theorem")
combined = "\n".join([doc, artifact_text])
for token in ["Restricted H4.1/FGL witness only", "restricted-domain bridge only", "finite-support measure package only", "unrestricted Chronos-RR remains FRONTIER_OPEN", "no unrestricted Chronos-RR", "no unrestricted H4.1/FGL theorem-level closure", "no Clay-problem closure"]:
    if token not in combined:
        raise SystemExit(f"missing boundary token: {token}")
for forbidden in ["unrestricted Chronos-RR is proved", "unrestricted Chronos-RR proved", "unrestricted Chronos-RR closed", "H4.1/FGL is solved", "H4.1/FGL solved", "H4.1/FGL is proved", "unrestricted H4.1/FGL is proved", "P vs NP is solved", "Clay problem is solved"]:
    if forbidden in combined or forbidden in lean:
        raise SystemExit(f"forbidden overclaim present: {forbidden}")
print("Restricted Chronos-RR to restricted H4.1/FGL verified.")
