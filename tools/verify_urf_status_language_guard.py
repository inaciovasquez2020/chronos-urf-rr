from pathlib import Path


CHECKED_FILES = [
    Path("docs/status/URF_REPOSITORY_STATUS_SEED_2026_04_28.json"),
    Path("docs/status/URF_REPOSITORY_STATUS_EXPORT_2026_04_28.md"),
]

REQUIRED_BOUNDARY_PHRASES = [
    "Build success verifies artifact integrity only",
    "does not imply theorem-level closure",
]

FORBIDDEN_PHRASES = [
    "Millennium solved",
    "Clay solved",
    "verified proof",
    "unconditional closure",
    "proved Clay",
    "proved Millennium",
    "final theorem claim",
]

ALLOWED_STATUS_PHRASES = [
    "Solved theorem surface",
    "Closed executable surface with placeholders",
    "Conditional result",
    "Open formalization",
    "Documentation / metadata only",
    "Archive candidate",
]


def fail(message):
    raise SystemExit(f"URF status language guard failed: {message}")


def main():
    for path in CHECKED_FILES:
        if not path.exists():
            fail(f"missing checked file: {path}")

        text = path.read_text(encoding="utf-8")

        for phrase in REQUIRED_BOUNDARY_PHRASES:
            if phrase not in text:
                fail(f"{path} missing required boundary phrase: {phrase}")

        lowered = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in lowered:
                fail(f"{path} contains forbidden phrase: {phrase}")

    export = Path("docs/status/URF_REPOSITORY_STATUS_EXPORT_2026_04_28.md")
    export_text = export.read_text(encoding="utf-8")

    if not any(phrase in export_text for phrase in ALLOWED_STATUS_PHRASES):
        fail("export contains no recognized status phrase")

    print("URF status language guard PASS")


if __name__ == "__main__":
    main()
