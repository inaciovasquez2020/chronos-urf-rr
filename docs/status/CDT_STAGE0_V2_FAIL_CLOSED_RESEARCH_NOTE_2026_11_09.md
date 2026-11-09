# CDT Stage 0 v2: row-level fail-closed correction (draft)

This branch is stacked **on PR #1335 at exact head `93a32286f67c2ec6730fce832b1ecddc4fc05d49`** and is deliberately not merged into the locked v1 protocol or `main`.

- Reject invalid parameter types, nonfinite or nonpositive (u_c) and threshold.
- Reject nonfinite or nonnumeric (eta), even in excluded rows; do not silently discard malformed, unknown, or duplicated metadata without review.
- Reject nonfinite derived means, swap estimator, null estimator, reversal product and null-control threshold; return `INVALID_INPUT` instead of a false candidate or uncaught arithmetic error.
- Require at least four *accepted synthetic rows* for every configuration; otherwise `PENDING`. This is a **software conservatism, not** a verified 16-block protocol, accepted hours, or independence/replication test.
- Every output explicitly records `execution_scope=SYNTHETIC_ONLY`. A result named `SINGLE_LAB_CANDIDATE_ONLY` is still **not** an experimental observation.
- Preserve the v2 individual C3/C4 null rejection and familiar output fields.

## Remaining obligations
The July 12 v1 algorithm and preregistration stay immutable. The independent within-control cancellation scenario `C3=[1e-4,-1e-4,0,0]` **still passes**, intentionally recorded by the adversarial test. A robust drift/outlier criterion would change the statistical acceptance rule and requires separately reviewed protocol authorization. This change does NOT authenticate block IDs, six accepted hours per block, the sealed blind key, source digests, G1–G5, or actual instrument data.

Tests: run both `python3 -B -m unittest discover -s tests -p 'test_cdt_stage0_classifier_v2*.py' -v` (repo Python path). The new suite includes 21 tests and 10,000 seeded cases. Neither CI green nor synthetic-case acceptance proves a physical effect.

**PR_REVIEW := PENDING; PHYSICAL_EXECUTION := NOT_AUTHORIZED; PRODUCTION_PREFLIGHT := OPEN.**

## Additional numerical audit (2026-11-09)

Sign reversal is evaluated through direct comparisons rather than multiplication because `1.2e-7 * (-1e-320)` underflows to `-0.0` in binary64; a product-based `<0` check reports a false negative although both means have opposite signs. The separate product calculation remains a conservative finiteness/overflow guard. Two isolated regressions cover signed subnormal means and exact-zero controls. The frozen experiment is unchanged.
