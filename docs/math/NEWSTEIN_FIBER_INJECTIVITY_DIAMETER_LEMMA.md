# Newstein Fiber Injectivity Diameter Lemma

Status: OPEN

## Statement

Fix distinct vertices \(u\neq v\). Let
\[
c_u\in Z_1(B_r(u);\mathbf F_2),\qquad c_v\in Z_1(B_r(v);\mathbf F_2).
\]
Assume
\[
\iota_u(c_u)=\iota_v(c_v)
\]
in the global quotient.

Then every \(2\)-chain \(S\) with
\[
\partial S=c_u-c_v
\]
must satisfy
\[
\operatorname{diam}(\operatorname{supp} S)>L.
\]

Equivalently, there is no \(L\)-bounded filling of a nonzero cross-fiber difference.

## Role

This is the weakest sufficient bridge from the local rank gap to the global direct-sum embedding.

## Consequence

If this lemma holds, then for \(u\neq v\),
\[
\iota_u([c_u])=\iota_v([c_v])
\Longrightarrow
[c_u]=0=[c_v]
\]
in the corresponding fiber quotients, so the fiber images embed as a direct sum in the global quotient.

## Dependencies

- docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_COMPUTATION_THEOREM.md
- docs/math/NEWSTEIN_GLOBAL_QUOTIENT_GAP_ASSEMBLY_THEOREM.md
- docs/math/SIMSLV_ROOTED_LOCAL_EXACTNESS_CLOSURE.md

## Finish condition

Replace this OPEN lemma by a theorem-level proof that any filling chain witnessing equality of two distinct fiber classes must have support diameter \(>L\).
