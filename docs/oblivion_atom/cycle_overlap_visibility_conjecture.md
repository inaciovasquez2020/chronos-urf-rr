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

Empirical witness classes include random \(4\)-regular graphs and random lifts of the theta graph.

## Corrected conjectural bridge

The false implication

\[
\mathrm{COR}(G)=\Omega(n)\Rightarrow \#\mathrm{FO}^2\text{-types}=\Omega(n)
\]

is replaced by the following strengthened statement.

## Conjecture

For each bounded degree bound \(\Delta\), there exist integers \(k_0 \ge 3\) and \(R_0 \ge 1\) such that for every bounded-degree graph family \(G_n\) with degree at most \(\Delta\),

\[
\mathrm{COR}_{R_0}(G_n)=\Omega(|V(G_n)|)
\Rightarrow
\#\mathrm{FO}^{k_0}_{R_0}\text{-local types}(G_n)=\Omega(|V(G_n)|).
\]

## Program role

This is the corrected visibility bridge needed to pass from linear cycle-overlap rank to local definable diversity and hence to EntropyDepth lower bounds.

## Immediate test target

Determine whether the implication already holds for

\[
k_0=3.
\]
