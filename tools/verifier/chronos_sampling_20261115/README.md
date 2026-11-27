# Chronos sampling: November 15 research certificates

**Evidence archive, not a claim of solved Minkowski sampling stability.**

This directory preserves 15 original Python source files and nine associated November 15 research notes, copied without modifying original bytes. The archive deliberately remains separate from PR #1358 (November 14 certificates).

## Executable research artifacts

- `exact/`: 13 scripts with exact-arithmetic finite checks or geometric reductions. `chronos_exact_N_K_reduction_certificate_20261115.py` requires SymPy; its result is not included in minimal CI replay.
- `exploratory/`: two finite-numerical investigations requiring NumPy and, for the Sobol QMC study, SciPy.

`verify_nov15.py` compares SHA-256 hashes of all 15 scripts and nine notes; it runs the 12 dependency-free scripts under Python `-E -B`. It rejects missing or altered files, nonzero exit codes and timeouts. Output from a numerical test is never a proof of an unrestricted limit. The three dependency-gated scripts are preserved and hash-checked but explicitly **NOT_RUN** by minimal CI.

The original complete ZIP archive `chronos_research_nov15_consolidated_candidate.zip` also contains historical execution receipts and manifests; those metadata files are not committed here because the branch's hash-pinned verifier supersedes them. Some research notes refer to additional standalone prototype scripts (full-prefix, tip, successor-rank) which were **not available as source attachments**; those code artifacts are not claimed to be reproduced or included in this branch. The associated mathematical notes are preserved.

## Audit boundaries

- Exact four-point Minkowski `p_(4,2)`: **OPEN**. Exact rational bounds and the one-scalar overlap reduction are not exact evaluation.
- Infinite-growth sampling-stability double limit: **OPEN**. Counterexamples concern other poset families, not typical Minkowski sprinklings.
- First-choice delocalization and extension-weight asymptotics: **OPEN**.
- Claimed predecessor-count concentration and Poisson tip limit: analytical proofs in notes; independent mathematical review **NOT_ESTABLISHED**.
- `Lean` compilation and `#print axioms`: **NOT_RUN**.
- Published Fishburn inequality input: Chan--Pak, *Correlation Inequalities for Linear Extensions*, Theorem 1.1; see https://www.math.ucla.edu/~pak/papers/Correlation13.pdf.
- Novelty: **NOT_ESTABLISHED**.
- Mac authoritative HEAD / local uncommitted work: **NOT_INSPECTED**.

All files in this branch are additions. Do not overwrite, reset or delete any local files or merge the research branch without explicit approval. A green exact-script CI establishes reproducibility under code assumptions, not independent kernel-verification or mathematical review.
