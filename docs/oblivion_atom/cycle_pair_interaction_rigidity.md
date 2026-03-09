# Cycle-Pair Interaction Rigidity

## Refined invariant

Define
\[
\mathrm{COR}^{\dagger}(G)
:=
\bigl(
\rank_{\mathbf F_2}(A_{\mathrm{cycle\text{-}edge}}),
\rank_{\mathbf F_2}(A_{\mathrm{cycle\text{-}intersection}}),
\rank_{\mathbf F_2}(A_{\mathrm{cycle\text{-}pair}})
\bigr).
\]

Here:

- \(A_{\mathrm{cycle\text{-}edge}}\) is the cycle-basis edge-incidence matrix;
- \(A_{\mathrm{cycle\text{-}intersection}}\) is the adjacency matrix of the cycle-intersection graph;
- \(A_{\mathrm{cycle\text{-}pair}}\) is the parity interaction matrix of cycle-pair overlaps.

## Candidate rigidity statement

There exists \(k_0\ge 5\) and \(R_0\ge 1\) such that
\[
\mathrm{COR}^{\dagger}_{R_0}(G_n)=\Omega(|V(G_n)|)
\Longrightarrow
\#\mathrm{FO}^{k_0}_{R_0}\text{-types}(G_n)=\Omega(|V(G_n)|).
\]

## Canonical obstruction family

Theta-random-lift families remain the canonical adversarial family for testing whether raw cycle rank, pair signatures, and interaction ranks still collapse under bounded-variable visibility.

## Immediate test protocol

For each family \(G_n\), record:
\[
\frac{\rank(A_{\mathrm{cycle\text{-}edge}})}{|V(G_n)|},\qquad
\frac{\rank(A_{\mathrm{cycle\text{-}intersection}})}{|V(G_n)|},\qquad
\frac{\rank(A_{\mathrm{cycle\text{-}pair}})}{|V(G_n)|}.
\]
