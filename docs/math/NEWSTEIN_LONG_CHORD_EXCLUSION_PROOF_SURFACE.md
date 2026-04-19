# Newstein Long-Chord Exclusion Proof Surface

Status: OPEN

## Statement

Let
\[
\sigma_i=e_i+P_T(e_i)\qquad (i=1,2),
\]
with \(e_1,e_2\) the long chords selected by the maximal-separation criterion.

The theorem-level target is:
\[
\forall i\in\{1,2\},\ \forall w\in W^{\mathrm{triv}},
\qquad
e_i\notin \operatorname{supp}(w).
\]

Equivalently,
\[
W^{\mathrm{triv}}
\subseteq
\operatorname{span}_{\mathbf F_2}\{\partial\tau:\tau\in\Phi_2^{\mathrm{triv}}\}
\]
contains no \(1\)-chain whose support contains either \(e_1\) or \(e_2\).

## Role

This is the exact theorem-level proof surface for the sigma-package exclusion step.

## Dependencies

- docs/math/NEWSTEIN_LONG_CHORD_EXCLUSION_LEMMA.md
- docs/math/NEWSTEIN_TWISTED_CONSTRAINTS_SIGMA12.md
- docs/math/SIMSLV_ROOTED_LOCAL_EXACTNESS_CLOSURE.md

## Finish condition

Replace this OPEN surface by a theorem-level derivation that every trivial witness boundary avoids both long chords.
