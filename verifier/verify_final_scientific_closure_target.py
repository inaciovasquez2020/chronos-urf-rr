#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/status/final_scientific_closure_target_2026_06_09.json"
DOC = ROOT / "docs/status/FINAL_SCIENTIFIC_CLOSURE_TARGET_2026_06_09.md"
REQUIRED_OBJECT = "final_scientific_closure"
REQUIRED_STATUS = "TARGET_ONLY"

def main() -> None:
    assert ARTIFACT.exists(), f"missing artifact: {ARTIFACT}"
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert data["object"] == REQUIRED_OBJECT
    status = data.get("status", data.get("route_status"))
    assert status == REQUIRED_STATUS
    boundary = "\n".join(data.get("boundary", []))
    assert "final scientific closure" in boundary
    assert DOC.exists(), f"missing doc: {DOC}"
    text = DOC.read_text(encoding="utf-8")
    assert REQUIRED_OBJECT in text
    assert "final_scientific_closure" in text
    print("FINAL_SCIENTIFIC_CLOSURE_TARGET_OK")

if __name__ == "__main__":
    main()
