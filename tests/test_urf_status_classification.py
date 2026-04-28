from tools.urf_status_classification import classify_repository, pressure_score


def test_axiom_free_verified_repo_is_solved_theorem_surface():
    result = classify_repository(
        {
            "sorry_count": 0,
            "admit_count": 0,
            "axiom_count": 0,
            "true_placeholder_count": 0,
            "verified_without_axioms": True,
        }
    )

    assert result["classification"] == "Solved theorem surface"


def test_boundary_markers_block_solved_classification():
    result = classify_repository(
        {
            "sorry_count": 0,
            "admit_count": 0,
            "axiom_count": 1,
            "true_placeholder_count": 0,
            "verified_without_axioms": True,
        }
    )

    assert result["classification"] != "Solved theorem surface"


def test_placeholders_classify_as_closed_executable_surface_with_placeholders():
    result = classify_repository(
        {
            "sorry_count": 0,
            "admit_count": 0,
            "axiom_count": 0,
            "true_placeholder_count": 4,
        }
    )

    assert result["classification"] == "Closed executable surface with placeholders"


def test_axioms_classify_as_conditional_result():
    result = classify_repository(
        {
            "sorry_count": 0,
            "admit_count": 0,
            "axiom_count": 3,
            "true_placeholder_count": 0,
        }
    )

    assert result["classification"] == "Conditional result"


def test_sorry_or_admit_classifies_as_open_formalization():
    result = classify_repository(
        {
            "sorry_count": 1,
            "admit_count": 0,
            "axiom_count": 0,
            "true_placeholder_count": 0,
        }
    )

    assert result["classification"] == "Open formalization"


def test_pressure_score():
    assert (
        pressure_score(
            {
                "sorry_count": 2,
                "admit_count": 3,
                "axiom_count": 4,
                "true_placeholder_count": 5,
                "trivial_proof_count": 6,
            }
        )
        == 100
    )
