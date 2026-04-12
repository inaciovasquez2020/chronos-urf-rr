# Newstein Coboundary Assembly Lemma

## Status
Conditional target.

## Lemma
Let \(U\) be a connected graph and let \(\phi:E(U)\to\mathbb F_2\).

Assume
\[
\phi(C)=0
\quad\text{for every cycle }C\subseteq U.
\]

Assume further:

1. the Newstein cycle-difference lemma;
2. the Newstein edge-coboundary verification lemma.

Then there exists
\[
f:V(U)\to\mathbb F_2
\]
such that
\[
\phi=\delta f.
\]

## Consequence
The Newstein coboundary assembly lemma discharges the Newstein local coboundary criterion modulo the two isolated sublemmas.

## Remaining proof obligations
1. invoke the cycle-difference lemma to obtain path-independence of the path integral defining \(f\);
2. invoke the edge-coboundary verification lemma to prove \(\phi(uv)=f(u)+f(v)\) on every edge;
3. substitute into the Newstein local coboundary criterion.

## Overclaim guard
No proof of the lemma is claimed here.
