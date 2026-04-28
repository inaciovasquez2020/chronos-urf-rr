FORBIDDEN_SOLVED_MARKERS = (
    "sorry_count",
    "admit_count",
    "axiom_count",
    "true_placeholder_count",
)


def _n(repo, key):
    return int(repo.get(key, 0) or 0)


def _b(repo, key):
    return bool(repo.get(key, False))


def pressure_score(repo):
    return (
        10 * _n(repo, "sorry_count")
        + 8 * _n(repo, "admit_count")
        + 6 * _n(repo, "axiom_count")
        + 4 * _n(repo, "true_placeholder_count")
        + 2 * _n(repo, "trivial_proof_count")
    )


def classify_repository(repo):
    sorry = _n(repo, "sorry_count")
    admit = _n(repo, "admit_count")
    axiom = _n(repo, "axiom_count")
    true_placeholder = _n(repo, "true_placeholder_count")
    lean_files = _n(repo, "lean_files")
    has_readme = _b(repo, "has_readme")
    has_tests = _b(repo, "has_tests")
    verified_without_axioms = _b(repo, "verified_without_axioms")

    if (
        sorry == 0
        and admit == 0
        and axiom == 0
        and true_placeholder == 0
        and verified_without_axioms
    ):
        classification = "Solved theorem surface"
        recommended_action = (
            "Preserve as strongest formal signal; add axiom-dependency guard."
        )
    elif sorry == 0 and admit == 0 and axiom == 0 and true_placeholder > 0:
        classification = "Closed executable surface with placeholders"
        recommended_action = (
            "Replace placeholders with real propositions or quarantine them."
        )
    elif axiom > 0 and sorry == 0 and admit == 0:
        classification = "Conditional result"
        recommended_action = (
            "Separate assumptions from theorem files and mark public status as conditional."
        )
    elif sorry > 0 or admit > 0:
        classification = "Open formalization"
        recommended_action = (
            "Eliminate sorry/admit markers before adding new theorem claims."
        )
    elif lean_files == 0 and has_readme:
        classification = "Documentation / metadata only"
        recommended_action = "Map claims to formal artifacts or mark as informal."
    elif lean_files == 0 and not has_tests:
        classification = "Archive candidate"
        recommended_action = (
            "Archive, consolidate, or keep private unless a concrete verification surface is added."
        )
    else:
        classification = "Unclassified"
        recommended_action = "Review repository status manually."

    if (
        classification == "Solved theorem surface"
        and sum(_n(repo, key) for key in FORBIDDEN_SOLVED_MARKERS) > 0
    ):
        classification = "Unclassified"
        recommended_action = (
            "Review repository status manually; solved classification is blocked by formal boundary markers."
        )

    out = dict(repo)
    out["classification"] = classification
    out["recommended_action"] = recommended_action
    out["pressure_score"] = pressure_score(repo)
    return out
