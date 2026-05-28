#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ART = ROOT / "artifacts/chronos/gdm_residual_identification_theorem_2026_05_28.json"
DOC = ROOT / "docs/status/GDM_RESIDUAL_IDENTIFICATION_THEOREM_2026_05_28.md"
LEAN = ROOT / "lean/Chronos/Frontier/GDMResidualIdentificationTheorem.lean"

required_paths = [ART, DOC, LEAN]
for path in required_paths:
    assert path.exists(), f"missing required file: {path}"

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data.get("artifact") == "GDM_RESIDUAL_IDENTIFICATION_THEOREM_V1"
assert data.get("status") == "FINITE_NONNEGATIVE_GDM_RESIDUAL_IDENTIFICATION_CLOSED"

for theorem in [
    "gdmResidualIdentification",
    "gdmResidualIdentification_nonnegative",
]:
    assert theorem in data.get("proved_theorems", []), theorem
    assert theorem in lean, theorem

required_boundary_tokens = [
    "finite nonnegative model only",
    "no observational evidence",
    "no galaxy rotation curve fit",
    "no lensing fit",
    "no empirical residual measurement",
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
]

combined = "\n".join([
    json.dumps(data, sort_keys=True),
    doc,
    lean,
])

for token in required_boundary_tokens:
    assert token in combined, token

assert "observedMass - baryonicMass" in combined
assert "geometric deficit mass" in combined
assert "GDM_RESIDUAL_IDENTIFICATION_THEOREM_V1" in combined

print("GDM_RESIDUAL_IDENTIFICATION_THEOREM_OK")
