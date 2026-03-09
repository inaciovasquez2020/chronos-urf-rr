# Cycle-Overlap Visibility Conjecture

## Empirical obstruction at FO^2 / WL^2

There exist bounded-degree graph families \(G_n\) such that
\[
\mathrm{COR}(G_n)=\Omega(n)
\]
while the WL\(^2\) / FO\(^2\) visibility proxy remains collapsed:
\[
\#\mathrm{Types}_{\mathrm{FO}^2}(G_n)=O(1).
\]

## Empirical obstruction at current FO^3 proxy

There exist bounded-degree graph families \(G_n\) such that
\[
\mathrm{COR}(G_n)=\Omega(n)
\]
while the current rooted-radius FO\(^3\) proxy remains collapsed:
\[
\#\mathrm{ProxyTypes}_{\mathrm{FO}^3}(G_n)=O(1).
\]

## Empirical obstruction at current FO^4 pair-signature proxy

For theta-random-lift families, the current FO\(^4\) pair-rooted proxy does not yet force linear vertex-visible diversity from raw cycle-overlap rank alone.

Accordingly, the relevant observable is not vertex-type diversity but pair-signature diversity.

## Refined invariant

Define
\[
\mathrm{COR}^{\ast}_{R}(G)
:=
\bigl(\mathrm{COR}_{R}(G),\,\Pi_{R}(G)\bigr),
\]
where
\[
\Pi_{R}(G)
\]
is the pair-rooted overlap-pattern profile extracted from exhaustive pair-signature multiplicities.

## Refined conjecture

For each bounded degree bound \(\Delta\), there exist integers \(R_0 \ge 1\) such that for every bounded-degree graph family \(G_n\) with degree at most \(\Delta\),
\[
\mathrm{COR}^{\ast}_{R_0}(G_n)=\Omega(|V(G_n)|)
\Rightarrow
\#\mathrm{PairSig}^{\mathrm{FO}^4}_{R_0}(G_n)=\Omega(|V(G_n)|).
\]

Here
\[
\#\mathrm{PairSig}^{\mathrm{FO}^4}_{R}(G)
\]
denotes the number of distinct pair-rooted FO\(^4\)-proxy signatures at radius \(R\).

## Canonical adversarial family

Theta-random-lift families are the canonical obstruction family for FO\(^2\), FO\(^3\), and current FO\(^4\)-proxy visibility tests.

## Immediate normalization targets

Record both
\[
\frac{\#\mathrm{PairSig}^{\mathrm{FO}^4}_{R}(G)}{|V(G)|}
\qquad\text{and}\qquad
\frac{\#\mathrm{PairSig}^{\mathrm{FO}^4}_{R}(G)}{|V(G)|^2}.
\]
