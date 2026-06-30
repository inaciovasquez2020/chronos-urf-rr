#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "restricted_package_theorem_surface_boundary_2026_06_30.json"

payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))

required = {
    "status": "negative_boundary",
    "boundary": "BOUNDARY := ¬ restricted_package_theorem_surface_closed",
    "open_gap": "restricted_package_theorem_surface_closed",
}

for key, expected in required.items():
    actual = payload.get(key)
    if actual != expected:
        raise SystemExit(f"restricted package theorem surface boundary mismatch: {key}: {actual!r}")

missing = payload.get("weakest_missing_object", "")
if "explicit restricted package theorem discharge" not in missing:
    raise SystemExit("restricted package theorem surface boundary does not name the weakest missing discharge")

hits = payload.get("source_search_hits", [])
if not hits:
    raise SystemExit("restricted package theorem surface boundary lacks source search hits")

forbidden = payload.get("forbidden_affirmative_claims", [])
if not forbidden:
    raise SystemExit("restricted package theorem surface boundary lacks forbidden affirmative claims")

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
                raise SystemExit(f"forbidden restricted package theorem closure claim found in {path}: {claim}")

print("RESTRICTED_PACKAGE_THEOREM_SURFACE_BOUNDARY_OK")
