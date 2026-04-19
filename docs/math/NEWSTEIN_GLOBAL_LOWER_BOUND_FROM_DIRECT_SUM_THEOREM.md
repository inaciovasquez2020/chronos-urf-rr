# Newstein Global Lower Bound from Direct-Sum Theorem

Status: OPEN

## Statement

Assume the Injectivity-to-Global Direct-Sum Theorem.

Let \(U\) be a family of pairwise distinct fibers, and for each \(u\in U\) let
\[
V_u\subseteq Z_1(B_r(u);\mathbf F_2)/W_u
\]
be a \(2\)-dimensional twisted subspace furnished by the sigma-package.

Then
\[
\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})
\ge
\dim_{\mathbf F_2}\Bigl(\bigoplus_{u\in U} V_u\Bigr)
=
2|U|.
\]

In particular, if \(|U|\to\infty\) along the graph family, then
\[
\dim_{\mathbf F_2}(Z_1/W^{\mathrm{glob}})\to\infty.
\]

## Role

This is the exact theorem-level lower-bound extraction from the global direct-sum embedding of the local sigma-fiber subspaces.

## Dependencies

- docs/math/NEWSTEIN_INJECTIVITY_TO_GLOBAL_DIRECT_SUM_THEOREM.md
- docs/math/NEWSTEIN_GLOBAL_QUOTIENT_LOWER_BOUND_FROM_SIGMA_FIBERS.md
- docs/math/NEWSTEIN_NON_FACTORIZATION_FROM_SIGMA_GROWTH.md

## Finish condition

Replace this OPEN theorem by a proof that the injective direct-sum embedding forces a \(2|U|\) lower bound on the global quotient dimension.
