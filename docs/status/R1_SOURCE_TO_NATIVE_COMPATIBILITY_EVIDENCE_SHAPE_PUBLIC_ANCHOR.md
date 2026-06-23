# R1_SOURCE_TO_NATIVE_COMPATIBILITY_EVIDENCE_SHAPE_PUBLIC_ANCHOR

STATUS := PUBLIC_BOUNDED_EXAMPLE_ANCHOR

REPOSITORY := chronos-urf-rr

MAIN_ANCHOR_COMMIT := a7a1bbcb

CLAIM := R1 source-to-native compatibility evidence shape is recorded as a bounded machine-checkable evidence-boundary example.

VERIFIER_COMMAND := `python3 tools/verify_r1_source_to_native_compatibility_evidence_shape.py`

PYTEST_COMMAND := `python3 -m pytest -q tests/test_r1_source_to_native_compatibility_evidence_shape.py`

BOUNDARY :=
- no R1 discharge claim
- no source-to-native compatibility theorem claim
- no compatibility evidence inhabitant claim
- no restricted continuation theorem claim
- no PDE analytic estimate closure claim
- no theorem-level URF closure claim
