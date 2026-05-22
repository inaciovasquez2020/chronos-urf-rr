#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/six_field_analytic_package_hypothesis_frontier_2026_05_22.json"
DOC = ROOT / "docs/status/SIX_FIELD_ANALYTIC_PACKAGE_HYPOTHESIS_FRONTIER_2026_05_22.md"
LEAN = ROOT / "lean/Chronos/Frontier/SixFieldAnalyticPackageHypothesisFrontier.lean"
IMPORT_FILE = ROOT / "Chronos.lean"

REQUIRED_TOKENS = [
    "SixFieldAnalyticPackageHypothesis",
    "RESTRICTED_PACKAGE_THEOREM_ONLY",
    "FRONTIER_OBJECT_ONLY_RESTRICTED_PACKAGE_THEOREM_NOT_PROMOTED",
    "unrestricted PDE well-posedness",
    "nonsymmetric evolution persistence",
    "admissibility preservation",
    "concentration transport",
    "finite-time collapse alternative",
    "unrestricted cosmic censorship",
    "unrestricted hoop theorem",
    "P vs NP",
    "any Clay problem",
]

FORBIDDEN_PROMOTIONS = [
    "proves unrestricted SixFieldAnalyticPackageHypothesis",
    "solves unrestricted SixFieldAnalyticPackageHypothesis",
    "proves unrestricted cosmic censorship",
    "solves unrestricted cosmic censorship",
    "proves unrestricted hoop theorem",
    "solves unrestricted hoop theorem",
    "proves P vs NP",
    "solves P vs NP",
    "proves any Clay problem",
    "solves any Clay problem",
]

def read(path: Path) -> str:
    assert path.exists(), f"missing file: {path}"
    return path.read_text()

def main() -> None:
    data = json.loads(read(ARTIFACT))
    doc = read(DOC)
    lean = read(LEAN)
    imports = read(IMPORT_FILE)
    combined = json.dumps(data, sort_keys=True) + "\n" + doc + "\n" + lean

    assert data["frontier_object"] == "SixFieldAnalyticPackageHypothesis"
    assert data["sole_frontier_object"] is True
    assert data["source_status"] == "RESTRICTED_PACKAGE_THEOREM_ONLY"
    assert data["theorem_promotion_lock"]["enabled"] is True
    assert "unrestricted SixFieldAnalyticPackageHypothesis" in data["does_not_prove"]
    assert len(data["obstruction_certificate"]["does_not_supply"]) == 5

    for token in REQUIRED_TOKENS:
        assert token in combined, f"missing token: {token}"

    for phrase in FORBIDDEN_PROMOTIONS:
        assert phrase not in combined, f"forbidden promotion phrase: {phrase}"

    assert "import Chronos.Frontier.SixFieldAnalyticPackageHypothesisFrontier" in imports

    print("SixFieldAnalyticPackageHypothesis frontier verification OK.")
    print(f"Status: {data['status']}")
    print(f"Source status: {data['source_status']}")
    print(f"Sole frontier object: {data['frontier_object']}")

if __name__ == "__main__":
    main()
