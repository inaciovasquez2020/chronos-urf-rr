# Cycle-Pair Interaction Rigidity

## Primary invariant

Define
\[
\mathrm{CPI}(G)
:=
\rank_{\mathbf F_2}(A_{\mathrm{cycle\text{-}pair}}),
\]
where \(A_{\mathrm{cycle\text{-}pair}}\) is the parity interaction matrix of cycle-basis overlaps.

## Empirical dichotomy

For random \(4\)-regular graphs:
\[
\mathrm{CPI}(G_n)=\Theta(n).
\]

For theta-random-lifts:
\[
\mathrm{CPI}(G_n)=0.
\]

Thus \(\mathrm{CPI}\) separates random regular families from the canonical theta-lift obstruction, whereas raw cycle-edge rank and cycle-intersection rank do not.

## Corrected conjecture

There exist \(k_0\ge 5\) and \(R_0\ge 1\) such that
\[
\mathrm{CPI}_{R_0}(G_n)=\Omega(|V(G_n)|)
\Longrightarrow
\#\mathrm{FO}^{k_0}_{R_0}\text{-types}(G_n)=\Omega(|V(G_n)|).
\]

## Canonical null-\(\mathrm{CPI}\) obstruction

Theta-random-lift families are the canonical obstruction family with
\[
\mathrm{CPI}(G_n)=0
\]
despite linear raw cycle rank.

## Immediate test protocol

For each family \(G_n\), record
\[
\frac{\mathrm{CPI}(G_n)}{|V(G_n)|}.
\]

Required comparison classes:

- random regular graphs,
- high-girth sparse graphs,
- random lifts of multiple base gadgets.
