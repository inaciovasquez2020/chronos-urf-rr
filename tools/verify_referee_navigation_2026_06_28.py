#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "REFEREE.md",
    "docs/referee/README.md",
    "docs/referee/REFEREE_MAP.md",
    "docs/referee/PROVEN_RESULTS.md",
    "docs/referee/CONDITIONAL_RESULTS.md",
    "docs/referee/ACCEPTANCE_SCOPE.md",
]

README_POINTERS = [
    "REFEREE_MAP.md",
    "PROVEN_RESULTS.md",
    "CONDITIONAL_RESULTS.md",
    "ACCEPTANCE_SCOPE.md",
]


def main() -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            raise SystemExit(f"MISSING_OBJECT := {rel}")

    referee = (ROOT / "REFEREE.md").read_text()
    if "docs/referee/README.md" not in referee:
        raise SystemExit("MISSING_OBJECT := REFEREE.md pointer to docs/referee/README.md")

    readme = (ROOT / "docs/referee/README.md").read_text()
    for name in README_POINTERS:
        if name not in readme:
            raise SystemExit(f"MISSING_OBJECT := docs/referee/README.md pointer to {name}")

    print("REFEREE_NAVIGATION_2026_06_28_OK")


if __name__ == "__main__":
    main()
