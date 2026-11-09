# 2026-11-09 URF manuscript archive: adversarial regression candidate

**Status:** ISOLATED_TESTED / NOT_PROMOTED. **Base:** remote draft PR #1338 (`research/urf-ai-readonly-audits-20261109`) at observed SHA `4bf390089640c78dc1563ea8555f80e528967c43`. No local Mac checkout, branch state, or dirty state was inspected. The integration branch contains only additive research fixtures and a read-only admission precheck; it does not change the authoritative Mac checkout or merge into main.

Original ZIP SHA-256: `f00830e566db256316e8eb2132f238882339c884d33504a8dd94696b7623a50e`.

## Mathematical scope

- Xystem paper: `Axioms/The_Xystem_Axiom__Global_Symmetry_and_Local_Spectral_Rigidity.pdf`. For `n > R`, `X_R(C_n)` has no 2-cells, and the nonzero eigenvalues of its edge 1-Laplacian equal those of `L(C_n)`. Thus `tr((Delta_1)^+) = (n^2 - 1)/12`, contrary to a uniform bound in all degree-2 vertex-transitive graphs. The exact finite test compares Gauss-Jordan inversion over `Fraction` with the independent closed-form identity for `n=5,8,12,16`.
- FO2 paper: `Rigidity/Explicit_Local_Cycle_Overlap_Rigidity_for_FO2_in_Bounded_Degree_Graphs.pdf`. The cubic vertex-transitive prism `C_n square K_2` has `n-1` distinct rectangular simple cycles sharing an edge. Vertex transitivity implies FO2 local homogeneity. The claimed uniform finite cycle-overlap threshold is therefore contradicted for sufficiently large `n`. Finite tests at `n=4,6,8,12` validate adjacency, transitivity automorphisms and explicit edge-sharing witnesses. They do **not** themselves reach the paper's (enormous) threshold.
- Both refutations require the accompanying general symbolic arguments; bounded calculations alone are **not** infinite-family proofs. Lean verification **NOT_RUN**.

## Fold-precheck policy

`finite_fold_precheck()` checks whether each *enumerated* fiber of a candidate `F` has constant `Sigma`. It accepts only a small bounded literal data representation, never reads PDFs or executes candidate-supplied code, and never writes repositories. All evidence is explicitly `FINITE_ENUMERATED_ONLY`; a completeness flag is only a **caller assertion**, not an independently verified domain certificate. Do not map any result to `PROVED` or `LEAN_VERIFIED`.

- Unsound merging: `REJECT_UNSOUND_FOLD`.
- Identity/injective candidate: `NO_NONTRIVIAL_REDUCTION_IN_CANDIDATE`, **not** `FORBIDDEN` or `UNSOLVABLE`.
- Missing coverage or excessive size: `INCOMPLETE`.
- Malformed input: `DEFER`.
- Consistent fibers and caller-asserted exhaustive finite domain: `SOUND_ON_ATTESTED_FINITE_DOMAIN`; this is not an unrestricted theorem.

**Known limitations:** Does not certify completeness, determine whether *any* alternative sound fold exists, evaluate the original decision functional outside supplied finite states, establish complexity lower bounds, or run Lean. Do not connect to the mutation adapter or proof ledger promotion. Review type semantics before widening allowed labels.

## Validation

From `tools/research-agent-toolkit/urf-ai`:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_archive_adversarial.py' -v
```

No third-party dependencies. Full RAT/URF-AI suite, project CI, security independent review, and proof assistant audit are **NOT_RUN** in this isolated test. Full-suite and repository CI status must be checked separately. No merge or Mac changes are performed by this patch.
