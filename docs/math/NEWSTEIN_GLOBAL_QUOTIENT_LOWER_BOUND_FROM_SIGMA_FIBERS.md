# Newstein Global Quotient Lower Bound from Sigma Fibers

Status: OPEN

## Statement

Assume the Global Direct-Sum Embedding Corollary.

Let \(U\) be a set of vertices such that for each \(u\in U\),
\[
\dim_{\mathbf F_2}\bigl(Z_1(B_r(u);\mathbf F_2)/W_u\bigr)\ge 2
\]
via the sigma-package twisted contribution.

Then
\[
\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\ge 2|U|.
\]

In particular, if \(|U|\) grows with the size of the ambient graph, then the global quotient dimension grows at least linearly in the number of sigma-fibers.

## Role

This is the exact global lower-bound consequence extracted from the direct-sum embedding of the local sigma-fibers.

## Dependencies

- docs/math/NEWSTEIN_GLOBAL_DIRECT_SUM_EMBEDDING_COROLLARY.md
- docs/math/NEWSTEIN_SIGMA_PACKAGE_DIMENSION_DROP.md
- docs/math/NEWSTEIN_GLOBAL_QUOTIENT_GAP_ASSEMBLY_THEOREM.md

## Finish condition

Replace this OPEN lower-bound package by a theorem-level derivation that each sigma-fiber contributes an independent \(2\)-dimensional summand to the global quotient.
