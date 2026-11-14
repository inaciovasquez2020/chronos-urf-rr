# Chronos sampling certificates — staged integration (2026-11-14)

**Scope:** finite combinatorial research evidence. The exact four-point Minkowski prefix probability and infinite-growth sampling-stability theorem remain **OPEN**. No Lean theorem or independent mathematical review is claimed.

## Provenance and scope

The source archive `chronos_sampling_certificates_candidate_20261114.zip` contains 18 scripts (9 primary, 6 supporting, 3 exploratory). Its integrity and execution were checked in an isolated Python environment. **This branch currently stages only 9 exact standard-library scripts**; 9 scripts remain outside the repository.

## Byte-preserved exact certificates

- `primary/chronos_insertion_transfer_exact_20261114.py`: SHA-256 `81393b324bff4c5871e5777314984f1866527dd6bb7e5a9d658df1d02b6cec12`; 219 four-element labeled orders × 4 deletion choices.
- `primary/chronos_overlap_decomposition_certificate.py`: SHA-256 `8f31bba39ee4a2f176e18168e3240ea7fe4962d0d78d1b535fbc987b0d8a68f6`; conditional moment identity and complete causal cuts.
- `primary/chronos_conditional_overlap_all_moments_20261114.py`: SHA-256 `5465bbb74c17b77d9ef42967ca42230ddc688ea6138c2d0b6b42c86a5665f634`; exact conditional moment checks.

- `supporting/chronos_comparable_pair_future_count_20261114.py`: SHA-256 `5b7817920be647bcb067bed94d210e09c8bc74b6a85a026b64094d8d46235b82`.
- `supporting/chronos_overlap_conditional_moment_audit_20261114.py`: SHA-256 `08c95a6c77d9ce0f06de0f00458813b6656bfdc406c47d244511a12ee2feef24`.
- `primary/chronos_symmetric_incomparable_overlap_exact_20261114.py`: SHA-256 `e23a2a2c8962c983ee7fd452fbfe5f506978641ce51bf53d055f49561996363f`.

- `primary/chronos_prefix_signed_insertion_exact_20261114.py`: SHA-256 `0f6eb2209377ee38f8d6e1aeacea516d15285f96bd0d0e628f7df30dd610d50a`.
- `primary/chronos_overlap_rigorous_lower_bound_20261114.py`: SHA-256 `63daf938a9200683672703a5ec741f4946d41f5da18d7bc80173bc050965cc2a`.
- `supporting/chronos_four_event_bounds.py`: SHA-256 `38e563c671a059c3eca567eb5816b23e7059797ea52366959789c9e834000409`.

All nine blobs have been verified byte-for-byte against the source archive.

The `verify_staged_certificates.py` runner fails on missing scripts, hash mismatches, nonzero execution, and timeouts. It requires only Python standard library. This runner has **not** yet been executed on the remote branch.

## Acceptance

- Exact 4D Minkowski `p_{4,2}`: **OPEN**.
- Incomparable-pair common-future second moment: **OPEN**.
- Fixed-prefix uniqueness and double limit: **OPEN**.
- Lean 4.29.0 kernel compilation and axiom audit: **NOT_RUN**.
- Full repository tests and exact-HEAD GitHub CI: **NOT_RUN**.
- Independent mathematical review: **NOT_ESTABLISHED**.
- Full 18-script bundle integration: **INCOMPLETE**.

Retain the existing baseline `docs/research/RANDOM_LINEAR_EXTENSION_SAMPLING_AUDIT_20261112.md`; do not overwrite it. Before promotion, review the exact diff, independently audit mathematical hypotheses, verify reproducibility, and obtain explicit approval. Do not merge as a completed theorem.
