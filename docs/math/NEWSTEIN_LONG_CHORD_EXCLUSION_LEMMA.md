# Newstein Long-Chord Exclusion Lemma

Status: OPEN

## Statement

Let
\[
\sigma_i=e_i+P_T(e_i)\qquad (i=1,2),
\]
where \(e_1,e_2\) are the long chords selected by the maximal-separation criterion in the rooted trivial witness layer.

Then
\[
\forall i\in\{1,2\},\ \forall w\in W^{\mathrm{triv}},
\qquad
e_i\notin \operatorname{supp}(w).
\]

Equivalently,
\[
W^{\mathrm{triv}}
\subseteq
\operatorname{span}_{\mathbf F_2}\{\partial\tau:\tau\in \Phi_2^{\mathrm{triv}}\}
\]
contains no \(1\)-chain whose support contains either \(e_1\) or \(e_2\).

## Role

This is the weakest sufficient missing lemma for the proposed \(\sigma\)-package.

## Consequences

From this lemma one obtains
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

## Dependencies

- docs/math/NEWSTEIN_TWISTED_CONSTRAINTS_SIGMA12.md
- docs/math/SIMSLV_ROOTED_LOCAL_EXACTNESS_CLOSURE.md
- docs/math/NEWSTEIN_FIBER_INJECTIVITY_DIAMETER_LEMMA.md

## Finish condition

Replace this OPEN lemma by a theorem-level proof that no trivial witness boundary can contain either long chord in its support.
