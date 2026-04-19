from pathlib import Path

REGISTRY = Path("OPEN_INPUTS_REGISTRY.md").read_text(encoding="utf-8")
SNAPSHOT = Path("STATUS_SNAPSHOT.md").read_text(encoding="utf-8")


def test_registry_status_is_conditional() -> None:
    assert "**Repository Status: CONDITIONAL**" in REGISTRY


def test_snapshot_status_is_conditional() -> None:
    assert "**CONDITIONAL**" in SNAPSHOT


def test_snapshot_separates_assembly_from_theorem() -> None:
    assert "## Assembly Layer" in SNAPSHOT
    assert "**COMPLETE**" in SNAPSHOT
    assert "## Theorem Layer" in SNAPSHOT
    assert "**INCOMPLETE**" in SNAPSHOT


def test_registry_contains_exact_terminal_inputs() -> None:
    assert "## (R1) Long-Chord Exclusion Lemma" in REGISTRY
    assert "## (R2) Diameter-Separation Filling Obstruction" in REGISTRY
    assert "## (R3) Uniform Local-Type Capacity Lemma" in REGISTRY


def test_downstream_r2_includes_sigma_package() -> None:
    needle = "(R2) + (R1) + sigma-package assembly ⟹ dim(Z₁ / W^glob) ≥ 2|U|"
    assert needle in REGISTRY or needle.replace(" / ", "/") in REGISTRY


def test_downstream_r3_explicit_form() -> None:
    assert "(R3) + (dim(Z₁/W^glob) ≥ 2|U|) + (|U| → ∞) ⟹ non-factorization" in REGISTRY


def test_substeps_listed_in_registry() -> None:
    for token in [
        "(R1a)", "(R1b)", "(R1c)",
        "(R2a)", "(R2b)", "(R2c)", "(R2d)",
        "(R3a)", "(R3b)", "(R3c)", "(R3d)",
    ]:
        assert token in REGISTRY


def test_no_unconditional_claims() -> None:
    assert "UNCONDITIONAL" not in REGISTRY
    assert "UNCONDITIONAL" not in SNAPSHOT


def test_nonfactorization_closure_requires_open_inputs() -> None:
    assert "non-factorization conclusion can be discharged" in REGISTRY
    assert "## (R1) Long-Chord Exclusion Lemma" in REGISTRY
    assert "## (R2) Diameter-Separation Filling Obstruction" in REGISTRY
    assert "## (R3) Uniform Local-Type Capacity Lemma" in REGISTRY
    assert REGISTRY.count("**Status: OPEN**") >= 3
