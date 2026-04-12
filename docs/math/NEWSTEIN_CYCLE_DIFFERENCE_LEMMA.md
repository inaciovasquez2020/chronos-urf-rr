# Newstein Cycle-Difference Lemma

## Status
Conditional target.

## Lemma
Let \(U\) be a connected graph, let \(x_0,x\in V(U)\), and let \(P,Q\) be two paths from \(x_0\) to \(x\).

Then the symmetric difference
\[
P\oplus Q
\]
is an \(\mathbb F_2\)-cycle in \(U\).

Consequently, if \(\phi:E(U)\to \mathbb F_2\) satisfies
\[
\phi(C)=0
\quad\text{for every cycle }C\subseteq U,
\]
then
\[
\sum_{e\in P}\phi(e)=\sum_{e\in Q}\phi(e).
\]

## Consequence
The cycle-difference lemma supplies the path-independence step in the Newstein path-integration lemma.

## Remaining proof obligations
1. verify every interior vertex of \(P\oplus Q\) has even \(\mathbb F_2\)-degree;
2. verify the endpoints \(x_0,x\) cancel modulo \(2\);
3. apply cycle-vanishing of \(\phi\).

## Overclaim guard
No proof of the lemma is claimed here.
