# R1_SOURCE_TO_NATIVE_COMPATIBILITY_INVARIANT_TARGET_BRIDGE_PUBLIC_ANCHOR

STATUS := PUBLIC_BOUNDED_EXAMPLE_ANCHOR

REPOSITORY := chronos-urf-rr

MAIN_ANCHOR_COMMIT := f7c361a5

CLAIM := R1 source-to-native compatibility invariant target bridge is recorded as a bounded machine-checkable bridge-scope example.

VERIFIER_COMMAND := `python3 tools/verify_r1_source_to_native_compatibility_invariant_target_bridge.py`

PYTEST_COMMAND := `python3 -m pytest -q tests/test_r1_source_to_native_compatibility_invariant_target_bridge.py`

BOUNDARY :=
- no R1 discharge claim
- no source-to-native compatibility theorem claim
- no compatibility evidence inhabitant claim
- no bridge-supplied forbidden compatibility evidence claim
- no restricted continuation theorem claim
- no theorem-level URF closure claim
