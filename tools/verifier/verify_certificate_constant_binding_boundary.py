#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "certificate_constant_binding_boundary_2026_06_30.json"

payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))

required = {
    "status": "negative_boundary",
    "boundary": "BOUNDARY := ¬ certificate_constant_binding",
    "open_gap": "certificate_constant_binding",
}

for key, expected in required.items():
    actual = payload.get(key)
    if actual != expected:
        raise SystemExit(f"certificate constant binding boundary mismatch: {key}: {actual!r}")

missing = payload.get("weakest_missing_object", "")
if "trusted explicit constant family" not in missing or "certificate checker" not in missing:
    raise SystemExit("certificate constant binding boundary does not name the weakest missing object")

forbidden = payload.get("forbidden_affirmative_claims", [])
if not forbidden:
    raise SystemExit("certificate constant binding boundary lacks forbidden affirmative claims")

search_roots = [
    ROOT / "artifacts",
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
                raise SystemExit(f"forbidden certificate constant binding closure claim found in {path}: {claim}")

print("CERTIFICATE_CONSTANT_BINDING_BOUNDARY_OK")
