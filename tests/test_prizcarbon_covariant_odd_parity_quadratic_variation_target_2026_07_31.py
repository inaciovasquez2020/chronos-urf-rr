from importlib.util import (
    module_from_spec,
    spec_from_file_location,
)
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = (
    ROOT
    / "tools"
    / "verify_prizcarbon_covariant_odd_parity_quadratic_variation_target_2026_07_31.py"
)


def load_verifier_module():
    spec = spec_from_file_location(
        "prizcarbon_quadratic_variation_target",
        VERIFIER,
    )

    assert spec is not None
    assert spec.loader is not None

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_current_action_metric_boundary() -> None:
    module = load_verifier_module()
    report = module.inspect_repository(ROOT)

    assert report["scalar_fields"] == (
        report["expected_scalar_fields"]
    )
    assert report["action_domain_is_scalar_record"]
    assert not report["action_file_mentions_odd_metric"]
    assert report["master_extraction_present"]
    assert report["second_metric_jet_present"]
    assert report["missing_metric_to_scalar_map"]
    assert report["missing_second_metric_variation"]
    assert not report["ready_for_metric_hessian"]


def test_target_contains_no_proof_hole_tokens() -> None:
    text = VERIFIER.read_text(encoding="utf-8")

    forbidden_tokens = [
        "ax" + "iom ",
        "op" + "aque",
        "sor" + "ry",
        "ad" + "mit",
    ]

    assert "structure Proposed" not in text
    assert all(
        token not in text
        for token in forbidden_tokens
    )
