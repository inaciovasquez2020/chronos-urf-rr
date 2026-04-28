import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.urf_status_classification import classify_repository


SEED = Path("docs/status/URF_REPOSITORY_STATUS_SEED_2026_04_28.json")
OUT = Path("docs/status/URF_REPOSITORY_STATUS_EXPORT_2026_04_28.md")

BOUNDARY = (
    "Build success verifies artifact integrity only. "
    "It does not imply theorem-level closure."
)

FORBIDDEN_PUBLIC_PHRASES = (
    "Millennium solved",
    "Clay solved",
    "verified proof",
    "unconditional closure",
)


def _escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_rows():
    data = json.loads(SEED.read_text(encoding="utf-8"))
    rows = [classify_repository(row) for row in data["repositories"]]
    return sorted(rows, key=lambda r: (-int(r["pressure_score"]), r["name"]))


def render_markdown():
    rows = build_rows()

    lines = [
        "# URF Repository Status Export — 2026-04-28",
        "",
        BOUNDARY,
        "",
        "Conditional repositories are explicitly marked as conditional. Open formalizations are explicitly marked as open.",
        "",
        "| Repository | Classification | Theorems | Lemmas | Axioms | Sorries | Admits | True placeholders | Verified without axioms | Pressure | Recommended next action |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape(row.get("name", "")),
                    _escape(row.get("classification", "")),
                    _escape(row.get("theorem_count", 0)),
                    _escape(row.get("lemma_count", 0)),
                    _escape(row.get("axiom_count", 0)),
                    _escape(row.get("sorry_count", 0)),
                    _escape(row.get("admit_count", 0)),
                    _escape(row.get("true_placeholder_count", 0)),
                    _escape(row.get("verified_without_axioms", False)),
                    _escape(row.get("pressure_score", 0)),
                    _escape(row.get("recommended_action", "")),
                ]
            )
            + " |"
        )

    lines.append("")
    return "\n".join(lines)


def main():
    text = render_markdown()

    for phrase in FORBIDDEN_PUBLIC_PHRASES:
        if phrase.lower() in text.lower():
            raise SystemExit(f"Forbidden public phrase detected: {phrase}")

    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
