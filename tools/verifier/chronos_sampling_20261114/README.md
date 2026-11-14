# Chronos sampling research certificates (2026-11-14)

**Scope: preserved finite mathematical and computational evidence only.** This research branch does **not** establish the exact four-event Minkowski random-prefix probability or infinite-growth sampling stability. Neither is presented as a Lean-verified theorem.

## Source provenance

All **18 original Python scripts** from the isolated `chronos_sampling_certificates_candidate_20261114.zip` are committed byte-for-byte, organized under:

- `primary/` — 9 analytical / exact finite-poset certificates, including one SciPy-dependent lens quadrature cross-check.
- `supporting/` — 6 exact rational supplementary audits.
- `exploratory/` — 3 numerical QMC investigations requiring NumPy and SciPy.

The original archive's SHA-256 values are pinned in `verify_staged_certificates.py`. All 18 corresponding Git blob hashes were independently compared with the archive and matched.

## Fail-closed execution gate

`verify_staged_certificates.py` checks the SHA-256 of **all 18** committed scripts, and replays the **14 standard-library** scripts. It rejects missing files, source changes, execution failures, and timeouts. The 4 dependency-gated scripts are hash-verified but intentionally marked NOT_RUN by that runner. Their earlier isolated-environment executions are **historical receipts**, not exact-HEAD GitHub CI results.

The fail-closed runner itself, repository-wide tests, pinned Lean 4.29.0, and exact-HEAD GitHub CI have not yet been observed running on this remote branch.

## Mathematical boundaries

- Exact four-point Minkowski `p_{4,2}`: **OPEN**; rational bounds are not an exact value.
- Full incomparable-pair common-future second moment: **OPEN**; local geometry and comparable-pair moments do not evaluate it.
- Uniqueness of the Minkowski finite-prefix limiting law and the `n→∞` outer limit: **OPEN**.
- Existing finite combinatorics: **COMPUTATION_PASS** for historical isolated execution, under the scripts' assumptions.
- Lean 4.29.0 compilation and `#print axioms`: **NOT_RUN** for these additions.
- Independent mathematical review and novelty: **NOT_ESTABLISHED**.
- Research status: **CERTIFICATE_ARCHIVE**, not a global theorem completion.

Keep `docs/research/RANDOM_LINEAR_EXTENSION_SAMPLING_AUDIT_20261112.md` unchanged as the existing baseline. These files supplement, not replace, the earlier audit.

## Promotion boundary

Before PR approval or merge: run and inspect the fail-closed runner on the exact branch SHA; confirm repository-wide checks and any formal Lean declarations with permitted axioms; review the exact diff, dependencies and claim statuses; preserve any local-only Mac research independently. The authoritative Mac working tree has not been inspected. A remote research branch is not evidence that local files are safe to overwrite or delete.
