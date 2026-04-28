import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.export_urf_status_public_table import (
    BOUNDARY,
    FORBIDDEN_PUBLIC_PHRASES,
    OUT,
    SEED,
    build_rows,
    render_markdown,
)


REQUIRED_REPOSITORIES = {
    "pachner-invariant",
    "cslib-fmt",
    "chronos-urf-rr",
    "urf-core",
    "urf-axioms",
    "poincare-new-derivation",
    "cyclone-terminal-obstruction",
}


def fail(message):
    raise SystemExit(f"URF status export verification failed: {message}")


def main():
    if not SEED.exists():
        fail(f"missing seed registry: {SEED}")

    data = json.loads(SEED.read_text(encoding="utf-8"))
    if data.get("status") != "status-only seed registry":
        fail("seed registry is not status-only")

    boundary = data.get("boundary", "")
    if "does not imply theorem-level closure" not in boundary:
        fail("seed registry boundary text missing theorem-level closure disclaimer")

    rows = build_rows()
    names = {row.get("name") for row in rows}

    missing = REQUIRED_REPOSITORIES - names
    if missing:
        fail(f"missing required seeded repositories: {sorted(missing)}")

    for row in rows:
        markers = (
            int(row.get("sorry_count", 0) or 0)
            + int(row.get("admit_count", 0) or 0)
            + int(row.get("axiom_count", 0) or 0)
            + int(row.get("true_placeholder_count", 0) or 0)
        )
        if markers > 0 and row.get("classification") == "Solved theorem surface":
            fail(f"boundary-marked repo classified as solved: {row.get('name')}")

    pressures = [int(row.get("pressure_score", 0) or 0) for row in rows]
    if pressures != sorted(pressures, reverse=True):
        fail("rows are not sorted by pressure descending")

    text = render_markdown()
    if BOUNDARY not in text:
        fail("export missing boundary text")

    for phrase in FORBIDDEN_PUBLIC_PHRASES:
        if phrase.lower() in text.lower():
            fail(f"forbidden public phrase detected: {phrase}")

    OUT.write_text(text, encoding="utf-8")

    if not OUT.exists():
        fail(f"export was not generated: {OUT}")

    print("URF status export verification PASS")


if __name__ == "__main__":
    main()
