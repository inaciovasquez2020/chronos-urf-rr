# R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_INHABITANT_PUBLIC_ANCHOR

STATUS := PUBLIC_BOUNDED_EXAMPLE_ANCHOR

REPOSITORY := chronos-urf-rr

MAIN_ANCHOR_COMMIT := d941fe41

CLAIM := R1 source-to-native compatibility evidence-inhabitant boundary is recorded as a bounded machine-checkable boundary example.

VERIFIER_COMMAND := `python3 tools/verify_r1_source_to_native_compatibility_evidence_shape_missing_inhabitant_boundary.py`

PYTEST_COMMAND := `python3 -m pytest -q tests/test_r1_source_to_native_compatibility_evidence_shape_missing_inhabitant_boundary.py`

BOUNDARY :=
- no R1 discharge claim
- no source-to-native compatibility theorem claim
- no compatibility evidence inhabitant construction claim
- no compatibility evidence discharge claim
- no restricted continuation theorem claim
- no theorem-level URF closure claim
