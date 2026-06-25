#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "external_validation" / "selected_domain_defect_basis_2026_06_24.json"
DOC = ROOT / "docs" / "status" / "SELECTED_DOMAIN_DEFECT_BASIS_2026_06_24.md"

def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    assert data["status_id"] == "SELECTED_DOMAIN_DEFECT_BASIS_2026_06_24"
    assert data["executable_simulation"] is False
    assert data["current_solve_percent"]["full_solve_estimate"] == 0.73
    assert data["closed_selected_layer"]["status"] == "closed"
    assert data["blocked_unrestricted_layer"]["status"] == "blocked"
    assert data["blocked_unrestricted_layer"]["first_blocker"] == "SELECTED_DOMAIN_DEFECT_BASIS"
    assert data["weakest_missing_object"]["name"] == "SELECTED_DOMAIN_DEFECT_BASIS"
    assert "BOUNDARY := ¬ unrestricted_terminal_closure_proved" in doc

    print("SELECTED_DOMAIN_DEFECT_BASIS_2026_06_24_OK")

if __name__ == "__main__":
    main()
