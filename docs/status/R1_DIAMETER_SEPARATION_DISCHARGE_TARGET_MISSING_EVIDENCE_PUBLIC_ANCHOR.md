# R1_DIAMETER_SEPARATION_DISCHARGE_TARGET_MISSING_EVIDENCE_PUBLIC_ANCHOR

STATUS := PUBLIC_BOUNDED_EXAMPLE_ANCHOR

REPOSITORY := chronos-urf-rr

MAIN_ANCHOR_COMMIT := ed2f66f2

CLAIM := R1 diameter separation discharge target is blocked by explicitly recorded missing evidence.

VERIFIER_COMMAND := `python3 tools/verify_r1_diameter_separation_discharge_target_missing_evidence_boundary.py`

PYTEST_COMMAND := `python3 -m pytest -q tests/test_r1_diameter_separation_discharge_target_missing_evidence_boundary.py`

BOUNDARY :=
- no R1 discharge claim
- no diameter separation theorem claim
- no missing evidence discharge claim
- no restricted continuation theorem claim
- no PDE analytic estimate closure claim
- no theorem-level URF closure claim
