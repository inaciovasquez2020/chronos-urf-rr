from pathlib import Path

from tools.export_urf_status_public_table import (
    BOUNDARY,
    FORBIDDEN_PUBLIC_PHRASES,
    OUT,
    build_rows,
    main,
    render_markdown,
)


def test_public_export_renders_boundary_text():
    text = render_markdown()

    assert BOUNDARY in text
    assert "does not imply theorem-level closure" in text


def test_public_export_contains_required_columns():
    text = render_markdown()

    assert "| Repository | Classification | Theorems | Lemmas | Axioms | Sorries | Admits | True placeholders | Verified without axioms | Pressure | Recommended next action |" in text


def test_public_export_is_sorted_by_pressure_descending():
    rows = build_rows()
    pressures = [row["pressure_score"] for row in rows]

    assert pressures == sorted(pressures, reverse=True)


def test_public_export_has_no_forbidden_public_phrases():
    text = render_markdown().lower()

    for phrase in FORBIDDEN_PUBLIC_PHRASES:
        assert phrase.lower() not in text


def test_public_export_file_is_generated():
    main()

    assert OUT.exists()
    text = OUT.read_text(encoding="utf-8")
    assert "URF Repository Status Export" in text
    assert "pachner-invariant" in text
    assert "chronos-urf-rr" in text
