#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "restricted_package_theorem_surface_boundary_2026_06_30.json"
TARGET = ROOT / "Chronos" / "Frontier" / "H4_1_FGL_FinalSelectedInputClosure.lean"

payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
target_text = TARGET.read_text(encoding="utf-8")

required = {
    "status": "restricted_surface_discharged",
    "boundary": "BOUNDARY := ¬ unrestricted H4.1/FGL",
    "closed_gap": "restricted_package_theorem_surface_closed",
    "open_gap": "unrestricted_h4_1_fgl",
    "discharge_theorem": "selected_observation_layer_to_named_restricted_package_surface",
}

for key, expected in required.items():
    actual = payload.get(key)
    if actual != expected:
        raise SystemExit(f"restricted package theorem surface status mismatch: {key}: {actual!r}")

required_target_fragments = [
    "def restricted_package_theorem_surface_closed : Prop :=",
    "theorem selected_observation_layer_to_named_restricted_package_surface :",
    "restricted_package_theorem_surface_closed := by",
    "H4_1_FGL_FinalSelectedInputClosure.ofInput I",
]

for fragment in required_target_fragments:
    if fragment not in target_text:
        raise SystemExit(f"missing restricted package theorem surface discharge fragment: {fragment}")

missing = payload.get("weakest_missing_object", "")
if "unrestricted H4.1/FGL" not in missing:
    raise SystemExit("restricted package theorem surface status does not preserve the unrestricted boundary")

forbidden = payload.get("forbidden_affirmative_claims", [])
if not forbidden:
    raise SystemExit("restricted package theorem surface status lacks forbidden unrestricted claims")

search_roots = [
    ROOT / "artifacts",
    ROOT / "Chronos",
    ROOT / "lean",
    ROOT / "scripts",
    ROOT / "tools",
]

for base in search_roots:
    if not base.exists():
        continue
    for path in base.rglob("*"):
        if not path.is_file() or path == ARTIFACT or path == Path(__file__).resolve():
            continue
        if ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for claim in forbidden:
            if claim in text:
                raise SystemExit(f"forbidden unrestricted H4.1/FGL closure claim found in {path}: {claim}")

print("RESTRICTED_PACKAGE_THEOREM_SURFACE_STATUS_OK")
