# Newstein Sigma-Package Dimension Drop

Status: OPEN

## Statement

Assume the Long-Chord Exclusion Lemma:
\[
\forall i\in\{1,2\},\ \forall w\in W^{\mathrm{triv}},
\qquad
e_i\notin \operatorname{supp}(w).
\]

Let
\[
\sigma_i=e_i+P_T(e_i)\qquad (i=1,2).
\]

Then
\[
\sigma_1,\sigma_2\notin W^{\mathrm{triv}},
\]
and
\[
a\sigma_1+b\sigma_2\in W^{\mathrm{triv}}
\Longrightarrow
a=b=0.
\]

Hence
\[
W^{\mathrm{tw}}
=
\operatorname{span}_{\mathbf F_2}(W^{\mathrm{triv}},\sigma_1,\sigma_2)
\]
satisfies
\[
\dim_{\mathbf F_2}(W^{\mathrm{tw}}/W^{\mathrm{triv}})=2.
\]

If additionally
\[
\dim_{\mathbf F_2}(Z_1/W^{\mathrm{triv}})=4,
\]
then
\[
\dim_{\mathbf F_2}(Z_1/W^{\mathrm{tw}})=2.
\]

## Role

This packages the exact rank-drop consequence of the \(\sigma\)-construction.

## Dependencies

- docs/math/NEWSTEIN_LONG_CHORD_EXCLUSION_LEMMA.md
- docs/math/NEWSTEIN_TWISTED_CONSTRAINTS_SIGMA12.md
- docs/math/NEWSTEIN_FIBER_QUOTIENT_RANK_COMPUTATION_THEOREM.md

## Finish condition

Replace this OPEN package by a theorem-level derivation of the \(4\to 2\) dimension drop from the long-chord exclusion input.
