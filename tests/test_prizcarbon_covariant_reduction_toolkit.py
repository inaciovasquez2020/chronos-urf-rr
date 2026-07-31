from pathlib import Path

from toolkit.prizcarbon_covariant_reduction import (
    audit_repository,
    contains_conditional_marker,
    normalize_text,
    primary_source_ids,
)


def test_identifier_normalization() -> None:
    assert normalize_text(
        "ProposedConditionalMasterCarrier"
    ) == "proposed conditional master carrier"

    assert normalize_text(
        "derivedReggeWheelerEquation"
    ) == "derived regge wheeler equation"

    assert contains_conditional_marker(
        "ProposedConditionalMasterCarrier"
    )


def test_primary_source_registry() -> None:
    source_ids = set(primary_source_ids())

    assert "regge_wheeler_1957" in source_ids
    assert "gerlach_sengupta_1980" in source_ids
    assert "martel_poisson_2005" in source_ids
    assert "tattersall_ferreira_lagos_2017" in source_ids


def test_conditional_and_concrete_classification(
    tmp_path: Path,
) -> None:
    frontier = (
        tmp_path
        / "lean"
        / "Chronos"
        / "Frontier"
    )
    frontier.mkdir(parents=True)

    (
        frontier / "ProposedMasterCarrier.lean"
    ).write_text(
        "\n".join(
            [
                "namespace Chronos.Frontier",
                "",
                "structure ProposedConditionalMasterCarrier where",
                "  masterEquation : ℝ → Prop",
                "",
                "end Chronos.Frontier",
                "",
            ]
        ),
        encoding="utf-8",
    )

    conditional_report = audit_repository(tmp_path)

    assert (
        conditional_report["stages"]
        ["master_equation"]
        ["status"]
        == "conditional_only"
    )

    (
        frontier / "DerivedOddParityEquation.lean"
    ).write_text(
        "\n".join(
            [
                "namespace Chronos.Frontier",
                "",
                "theorem derivedReggeWheelerEquation :",
                "    ReggeWheelerEquation = 0 := by",
                "  rfl",
                "",
                "end Chronos.Frontier",
                "",
            ]
        ),
        encoding="utf-8",
    )

    concrete_report = audit_repository(tmp_path)

    assert (
        concrete_report["stages"]
        ["master_equation"]
        ["status"]
        == "unqualified_evidence"
    )

    assert any(
        match["path"].endswith(
            "DerivedOddParityEquation.lean"
        )
        and match["tier"] == "unqualified"
        for match in concrete_report["stages"]
        ["master_equation"]
        ["matches"]
    )
