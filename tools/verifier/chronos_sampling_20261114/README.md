# Chronos sampling certificates — staged integration (2026-11-14)

**Scope:** finite combinatorial research evidence. The exact four-point Minkowski prefix probability and infinite-growth sampling-stability theorem remain **OPEN**. No Lean theorem or independent mathematical review is claimed.

## Provenance and scope

The source archive `chronos_sampling_certificates_candidate_20261114.zip` contains 18 scripts (9 primary, 6 supporting, 3 exploratory). Its integrity and execution were checked in an isolated Python environment. **This branch currently stages only 3 exact standard-library scripts**; 15 scripts remain outside the repository.

## Byte-preserved exact certificates

- `primary/chronos_insertion_transfer_exact_20261114.py`: SHA-256 `81393b324bff4c5871e5777314984f1866527dd6bb7e5a9d658df1d02b6cec12`; 219 four-element labeled orders × 4 deletion choices.
- `primary/chronos_overlap_decomposition_certificate.py`: SHA-256 `8f31bba39ee4a2f176e18168e3240ea7fe4962d0d78d1b535fbc987b0d8a68f6`; conditional moment identity and complete causal cuts.
- `primary/chronos_conditional_overlap_all_moments_20261114.py`: SHA-256 `5465bbb74c17b77d9ef42967ca42230ddc688ea6138c2d0b6b42c86a5665f634`; exact conditional moment checks.

All three blobs have been verified byte-for-byte against the source archive.

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
