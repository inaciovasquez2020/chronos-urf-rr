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

Theta-random-lift data currently yields constant proxy diversity.

## Corrected conjectural bridge

The implication
\[
\mathrm{COR}(G)=\Omega(n)\Rightarrow \#\mathrm{FO}^k\text{-types}=\Omega(n)
\]
cannot be asserted for \(k=2\), and is not supported by the current FO\(^3\) proxy.

## Refined conjecture

For each bounded degree bound \(\Delta\), there exist integers \(k_0 \ge 4\) and \(R_0 \ge 1\), together with a refined invariant
\[
\mathrm{COR}^{\ast}_{R_0}(G),
\]
such that for every bounded-degree graph family \(G_n\) with degree at most \(\Delta\),
\[
\mathrm{COR}^{\ast}_{R_0}(G_n)=\Omega(|V(G_n)|)
\Rightarrow
\#\mathrm{FO}^{k_0}_{R_0}\text{-local types}(G_n)=\Omega(|V(G_n)|).
\]

## Candidate refinement

A minimal candidate is
\[
\mathrm{COR}^{\ast}_{R}(G)
=
\bigl(\mathrm{COR}_{R}(G),\ \mathrm{OP}_{R}(G)\bigr),
\]
where \(\mathrm{OP}_{R}(G)\) records cycle-overlap pattern data not visible in raw cycle-basis rank alone.

## Immediate test target

Determine whether the implication already holds for
\[
k_0=4
\]
using pair-rooted radius signatures as an FO\(^4\)-proxy.
