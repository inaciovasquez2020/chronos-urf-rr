#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ARTIFACT = Path("artifacts/chronos/hep_t_external_notation_classification_2026_06_10.json")

EXPECTED_ID = "HEP_T_EXTERNAL_NOTATION_CLASSIFICATION_2026_06_10"


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    assert data["id"] == EXPECTED_ID
    assert data["status"] == "typed_external_notation_only"
    assert data["symbol"] == "t"
    assert data["domain"] == "High Energy Physics"

    classification = data["classification"]
    assert classification["included_in_unification_scope"] is True
    assert classification["included_as_core_unification_primitive"] is False
    assert classification["included_as_core_theorem_target"] is False
    assert classification["included_as_external_domain_notation"] is True

    meanings = {entry["meaning"]: entry["admissibility"] for entry in data["admissible_meanings"]}
    assert meanings["top quark"] == "external typed notation only"
    assert meanings["Mandelstam momentum-transfer variable"] == "external typed notation only"

    excluded = set(data["excluded_claims"])
    assert "top-quark physics theorem" in excluded
    assert "scattering-amplitude theorem" in excluded
    assert "QFT phenomenology expansion" in excluded
    assert "Mandelstam-variable analytic closure" in excluded

    assert data["unifying_object"] == [
        "symbol",
        "domain",
        "type",
        "admissibility_conditions",
        "source_payload",
    ]

    assert "does not claim HEP physics content" in data["boundary"]

    print("HEP_T_EXTERNAL_NOTATION_CLASSIFICATION_OK")


if __name__ == "__main__":
    main()
